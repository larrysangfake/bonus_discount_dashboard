"""
Dirk scraper for discount data.
Note: This is a template/placeholder implementation.
"""
from .base_scraper import BaseScraper, logger
from typing import List, Dict
from datetime import datetime, timedelta


class DirkScraper(BaseScraper):
    """Scraper for Dirk van den Broek discount data."""
    
    def __init__(self):
        super().__init__("Dirk")
        self.base_url = "https://www.dirk.nl"
    
    def scrape(self) -> List[Dict]:
        """
        Scrape discount data from Dirk.
        
        NOTE: Placeholder implementation with sample data.
        """
        logger.info(f"Starting scrape for {self.supermarket_name}")
        
        sample_data = [
            {
                'supermarket': self.supermarket_name,
                'product_name': 'Kipfilet 500g',
                'category': 'Vlees & Kip',
                'original_price': 5.49,
                'discount_price': 3.99,
                'discount_percentage': 27.32,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=7),
                'image_url': 'https://example.com/chicken.jpg',
                'product_url': f'{self.base_url}/producten/kip',
                'description': 'Week aanbieding',
                'is_active': True
            },
            {
                'supermarket': self.supermarket_name,
                'product_name': 'Tomaten Cherry 250g',
                'category': 'Groente & Fruit',
                'original_price': 1.99,
                'discount_price': 1.29,
                'discount_percentage': 35.18,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=3),
                'image_url': 'https://example.com/tomatoes.jpg',
                'product_url': f'{self.base_url}/producten/tomaten',
                'description': 'Superkorting',
                'is_active': True
            }
        ]
        
        logger.info(f"Scraped {len(sample_data)} discounts from {self.supermarket_name}")
        return sample_data
