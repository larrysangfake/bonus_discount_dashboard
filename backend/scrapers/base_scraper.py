"""
Base scraper class for supermarket discount scrapers.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for supermarket scrapers."""
    
    def __init__(self, supermarket_name: str):
        self.supermarket_name = supermarket_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Scrape discount data from the supermarket website.
        Returns a list of dictionaries with discount information.
        """
        pass
    
    def parse_price(self, price_str: str) -> float:
        """Parse price string to float."""
        try:
            # Remove currency symbols and convert comma to dot
            cleaned = price_str.replace('€', '').replace(',', '.').strip()
            return float(cleaned)
        except (ValueError, AttributeError):
            return 0.0
    
    def calculate_discount_percentage(self, original_price: float, discount_price: float) -> float:
        """Calculate discount percentage."""
        if original_price > 0:
            return round(((original_price - discount_price) / original_price) * 100, 2)
        return 0.0
    
    def get_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a webpage."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def close(self):
        """Close the session."""
        self.session.close()
