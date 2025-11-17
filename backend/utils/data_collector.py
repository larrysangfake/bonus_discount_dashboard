"""
Data collection utility to run scrapers and store data.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scrapers import SCRAPERS
from models import Discount, init_db, SessionLocal
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def collect_all_discounts():
    """Run all scrapers and store discount data in the database."""
    logger.info("Starting discount data collection")
    
    # Initialize database
    init_db()
    
    session = SessionLocal()
    total_saved = 0
    
    try:
        for scraper_name, scraper_class in SCRAPERS.items():
            logger.info(f"Running {scraper_name} scraper...")
            scraper = scraper_class()
            
            try:
                discounts = scraper.scrape()
                
                for discount_data in discounts:
                    discount = Discount(**discount_data)
                    session.add(discount)
                    total_saved += 1
                
                logger.info(f"Added {len(discounts)} discounts from {scraper_name}")
                
            except Exception as e:
                logger.error(f"Error scraping {scraper_name}: {e}")
                
            finally:
                scraper.close()
        
        session.commit()
        logger.info(f"Total discounts saved: {total_saved}")
        
    except Exception as e:
        logger.error(f"Error during collection: {e}")
        session.rollback()
        
    finally:
        session.close()


def clear_old_discounts():
    """Remove inactive or expired discounts from the database."""
    from datetime import datetime
    
    session = SessionLocal()
    try:
        # Mark discounts as inactive if their valid_until date has passed
        expired = session.query(Discount).filter(
            Discount.valid_until < datetime.now(),
            Discount.is_active == True
        ).update({Discount.is_active: False})
        
        session.commit()
        logger.info(f"Marked {expired} discounts as inactive")
        
    except Exception as e:
        logger.error(f"Error clearing old discounts: {e}")
        session.rollback()
        
    finally:
        session.close()


if __name__ == '__main__':
    collect_all_discounts()
    clear_old_discounts()
