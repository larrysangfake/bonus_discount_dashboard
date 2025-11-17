"""
Flask API for the discount dashboard.
Provides endpoints to query and filter discount data.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Discount, SessionLocal, init_db
from datetime import datetime
from sqlalchemy import or_, and_

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize database on startup
init_db()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/api/discounts', methods=['GET'])
def get_discounts():
    """
    Get all active discounts with optional filters.
    
    Query parameters:
    - supermarket: Filter by supermarket name
    - category: Filter by category
    - min_discount: Minimum discount percentage
    - search: Search in product name
    - limit: Maximum number of results (default: 100)
    - offset: Pagination offset (default: 0)
    """
    session = SessionLocal()
    
    try:
        # Start with base query for active discounts
        query = session.query(Discount).filter(Discount.is_active == True)
        
        # Apply filters
        supermarket = request.args.get('supermarket')
        if supermarket:
            query = query.filter(Discount.supermarket == supermarket)
        
        category = request.args.get('category')
        if category:
            query = query.filter(Discount.category == category)
        
        min_discount = request.args.get('min_discount', type=float)
        if min_discount:
            query = query.filter(Discount.discount_percentage >= min_discount)
        
        search = request.args.get('search')
        if search:
            query = query.filter(Discount.product_name.ilike(f'%{search}%'))
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        limit = request.args.get('limit', default=100, type=int)
        offset = request.args.get('offset', default=0, type=int)
        
        # Order by discount percentage (highest first)
        query = query.order_by(Discount.discount_percentage.desc())
        
        # Apply limit and offset
        discounts = query.limit(limit).offset(offset).all()
        
        return jsonify({
            'discounts': [d.to_dict() for d in discounts],
            'total': total,
            'limit': limit,
            'offset': offset
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    finally:
        session.close()


@app.route('/api/discounts/<int:discount_id>', methods=['GET'])
def get_discount(discount_id):
    """Get a specific discount by ID."""
    session = SessionLocal()
    
    try:
        discount = session.query(Discount).filter(Discount.id == discount_id).first()
        
        if not discount:
            return jsonify({'error': 'Discount not found'}), 404
        
        return jsonify(discount.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    finally:
        session.close()


@app.route('/api/supermarkets', methods=['GET'])
def get_supermarkets():
    """Get list of all supermarkets with active discounts."""
    session = SessionLocal()
    
    try:
        supermarkets = session.query(Discount.supermarket).filter(
            Discount.is_active == True
        ).distinct().all()
        
        return jsonify({
            'supermarkets': [s[0] for s in supermarkets]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    finally:
        session.close()


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get list of all categories with active discounts."""
    session = SessionLocal()
    
    try:
        categories = session.query(Discount.category).filter(
            Discount.is_active == True,
            Discount.category.isnot(None)
        ).distinct().all()
        
        return jsonify({
            'categories': sorted([c[0] for c in categories if c[0]])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    finally:
        session.close()


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about discounts."""
    session = SessionLocal()
    
    try:
        total_discounts = session.query(Discount).filter(Discount.is_active == True).count()
        
        # Get discount count by supermarket
        supermarket_counts = {}
        supermarkets = session.query(Discount.supermarket).filter(
            Discount.is_active == True
        ).distinct().all()
        
        for sm in supermarkets:
            supermarket_counts[sm[0]] = session.query(Discount).filter(
                Discount.supermarket == sm[0],
                Discount.is_active == True
            ).count()
        
        # Calculate average discount percentage
        avg_discount = session.query(Discount.discount_percentage).filter(
            Discount.is_active == True,
            Discount.discount_percentage.isnot(None)
        ).all()
        
        avg_discount_pct = sum([d[0] for d in avg_discount if d[0]]) / len(avg_discount) if avg_discount else 0
        
        return jsonify({
            'total_discounts': total_discounts,
            'supermarket_counts': supermarket_counts,
            'average_discount_percentage': round(avg_discount_pct, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    finally:
        session.close()


if __name__ == '__main__':
    import os
    # Only enable debug mode in development
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
