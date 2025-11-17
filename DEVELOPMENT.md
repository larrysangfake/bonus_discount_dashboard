# Development Guide

This guide will help you set up the development environment and understand the project structure.

## Project Overview

The Bonus Discount Dashboard is a full-stack application consisting of:

1. **Backend** (Flask API) - Serves discount data via REST API
2. **Frontend** (React) - User interface for browsing and filtering discounts
3. **Scrapers** - Data collection modules for each supermarket
4. **Database** (SQLite) - Stores discount information

## Architecture

```
┌─────────────┐     HTTP      ┌─────────────┐     ORM      ┌──────────┐
│   React     │ ───────────▶  │  Flask API  │ ───────────▶ │  SQLite  │
│  Frontend   │               │   Backend   │              │ Database │
└─────────────┘               └─────────────┘              └──────────┘
                                     │
                                     │ Uses
                                     ▼
                              ┌─────────────┐
                              │  Scrapers   │
                              └─────────────┘
```

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/larrysangfake/bonus_discount_dashboard.git
cd bonus_discount_dashboard
```

### 2. Quick Setup

Run the setup script to install all dependencies:

```bash
./setup.sh
```

Or follow the manual setup below.

### 3. Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python models/database.py

# Collect sample data
python utils/data_collector.py
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Option 1: Use Start Script (Recommended)

```bash
./start.sh
```

This will start both backend and frontend in the background.

To stop:

```bash
./stop.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**

```bash
cd backend
source venv/bin/activate
python api/app.py
```

**Terminal 2 - Frontend:**

```bash
cd frontend
npm start
```

### Option 3: Docker

```bash
docker-compose up
```

To rebuild:

```bash
docker-compose up --build
```

## Development Workflow

### Backend Development

1. **Making Changes to Models**

   Edit `backend/models/database.py`:

   ```python
   # Add new field to Discount model
   new_field = Column(String(100))
   ```

   Reinitialize database:

   ```bash
   python models/database.py
   ```

2. **Adding New API Endpoints**

   Edit `backend/api/app.py`:

   ```python
   @app.route('/api/new-endpoint', methods=['GET'])
   def new_endpoint():
       # Your code here
       return jsonify({'data': 'value'})
   ```

3. **Creating New Scrapers**

   Create `backend/scrapers/new_scraper.py`:

   ```python
   from .base_scraper import BaseScraper

   class NewScraper(BaseScraper):
       def __init__(self):
           super().__init__("New Supermarket")
           self.base_url = "https://www.newsupermarket.nl"
       
       def scrape(self):
           # Implement scraping logic
           return []
   ```

   Register in `backend/scrapers/__init__.py`:

   ```python
   from .new_scraper import NewScraper

   SCRAPERS = {
       # ... existing scrapers
       'new_supermarket': NewScraper
   }
   ```

### Frontend Development

1. **Adding New Components**

   Create in `frontend/src/components/NewComponent.js`:

   ```jsx
   import React from 'react';
   import './NewComponent.css';

   const NewComponent = ({ props }) => {
       return (
           <div className="new-component">
               {/* Component content */}
           </div>
       );
   };

   export default NewComponent;
   ```

2. **Modifying the API Service**

   Edit `frontend/src/services/api.js`:

   ```javascript
   export const newApiCall = async () => {
       try {
           const response = await api.get('/new-endpoint');
           return response.data;
       } catch (error) {
           console.error('Error:', error);
           throw error;
       }
   };
   ```

## API Documentation

### Available Endpoints

#### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-11-17T18:00:00.000000"
}
```

#### `GET /api/discounts`
Get all active discounts with optional filters.

**Query Parameters:**
- `supermarket` (string) - Filter by supermarket name
- `category` (string) - Filter by category
- `min_discount` (number) - Minimum discount percentage
- `search` (string) - Search in product name
- `limit` (number) - Maximum results (default: 100)
- `offset` (number) - Pagination offset (default: 0)

**Example:**
```bash
curl "http://localhost:5000/api/discounts?supermarket=Jumbo&min_discount=20"
```

**Response:**
```json
{
    "discounts": [...],
    "total": 42,
    "limit": 100,
    "offset": 0
}
```

#### `GET /api/discounts/:id`
Get a specific discount by ID.

#### `GET /api/supermarkets`
Get list of all supermarkets.

#### `GET /api/categories`
Get list of all categories.

#### `GET /api/stats`
Get statistics about discounts.

## Database Schema

### Discount Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| supermarket | String(50) | Supermarket name |
| product_name | String(255) | Product name |
| category | String(100) | Product category |
| original_price | Float | Original price |
| discount_price | Float | Discounted price |
| discount_percentage | Float | Discount percentage |
| valid_from | DateTime | Valid from date |
| valid_until | DateTime | Valid until date |
| image_url | String(500) | Product image URL |
| product_url | String(500) | Product page URL |
| description | String(1000) | Discount description |
| is_active | Boolean | Whether discount is active |
| created_at | DateTime | Record creation time |
| updated_at | DateTime | Last update time |

## Testing

### Testing the Backend

```bash
cd backend
source venv/bin/activate

# Test database initialization
python models/database.py

# Test data collection
python utils/data_collector.py

# Test API endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/discounts
curl http://localhost:5000/api/stats
```

### Testing the Frontend

```bash
cd frontend

# Run in development mode
npm start

# Build for production
npm run build
```

## Common Issues

### Port Already in Use

If port 5000 or 3000 is already in use:

```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill
```

### Database Locked

If you get a "database is locked" error:

```bash
# Stop all running processes
./stop.sh

# Remove database file and reinitialize
rm data/discounts.db
python backend/models/database.py
python backend/utils/data_collector.py
```

### CORS Errors

Ensure the backend has CORS enabled (already configured in `api/app.py`):

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use docstrings for functions and classes
- Type hints are encouraged

### JavaScript (Frontend)

- Use functional components with hooks
- Follow Airbnb JavaScript Style Guide
- Use meaningful variable names

## Directory Structure

```
bonus_discount_dashboard/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py              # Flask application
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py         # Database models
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py     # Base scraper class
│   │   ├── albert_heijn_scraper.py
│   │   ├── jumbo_scraper.py
│   │   ├── lidl_scraper.py
│   │   └── dirk_scraper.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── data_collector.py   # Data collection utility
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── DiscountCard.js
│   │   │   ├── DiscountCard.css
│   │   │   ├── FilterBar.js
│   │   │   └── FilterBar.css
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   └── Dashboard.css
│   │   ├── services/
│   │   │   └── api.js          # API service layer
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── Dockerfile
├── data/
│   ├── raw/
│   ├── processed/
│   └── discounts.db            # SQLite database
├── docker-compose.yml
├── setup.sh
├── start.sh
├── stop.sh
├── README.md
└── DEVELOPMENT.md
```

## Next Steps

1. **Implement Real Scrapers**: Replace placeholder scrapers with actual web scraping logic
2. **Add Tests**: Write unit and integration tests
3. **Improve UI**: Enhance the frontend design
4. **Add Features**: User accounts, saved searches, notifications
5. **Deploy**: Set up production deployment

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Getting Help

- Open an issue on GitHub
- Check existing issues for similar problems
- Review the README.md for quick start guides
