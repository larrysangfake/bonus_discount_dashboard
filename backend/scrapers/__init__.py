"""
Scrapers package initialization.
"""
from .albert_heijn_scraper import AlbertHeijnScraper
from .jumbo_scraper import JumboScraper
from .lidl_scraper import LidlScraper
from .dirk_scraper import DirkScraper

__all__ = ['AlbertHeijnScraper', 'JumboScraper', 'LidlScraper', 'DirkScraper']

# Registry of all available scrapers
SCRAPERS = {
    'albert_heijn': AlbertHeijnScraper,
    'jumbo': JumboScraper,
    'lidl': LidlScraper,
    'dirk': DirkScraper
}
