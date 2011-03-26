from spiders.delfi_comments import DelfiLtSpider
import unittest

class TestDelfiLtSpider(unittest.TestCase):
    """Tests main spider"""
    def test_spider_initiation(self):
        """tests if object instance can be created"""
        a = DelfiLtSpider()
    
    def test_link_selector(self):
        """tests if all the links selected 
        from the loader are of the r"(\d+)"
        """
        pass
        