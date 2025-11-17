"""
Database models for the discount dashboard.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Discount(Base):
    """Model for storing discount information from supermarkets."""
    __tablename__ = 'discounts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    supermarket = Column(String(50), nullable=False, index=True)
    product_name = Column(String(255), nullable=False)
    category = Column(String(100), index=True)
    original_price = Column(Float)
    discount_price = Column(Float, nullable=False)
    discount_percentage = Column(Float)
    valid_from = Column(DateTime)
    valid_until = Column(DateTime, index=True)
    image_url = Column(String(500))
    product_url = Column(String(500))
    description = Column(String(1000))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'supermarket': self.supermarket,
            'product_name': self.product_name,
            'category': self.category,
            'original_price': self.original_price,
            'discount_price': self.discount_price,
            'discount_percentage': self.discount_percentage,
            'valid_from': self.valid_from.isoformat() if self.valid_from else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'image_url': self.image_url,
            'product_url': self.product_url,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Database setup
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
DB_PATH = os.path.join(DB_DIR, 'discounts.db')

# Ensure data directory exists
os.makedirs(DB_DIR, exist_ok=True)

engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(engine)
    print(f"Database initialized at {DB_PATH}")

def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

if __name__ == '__main__':
    init_db()
