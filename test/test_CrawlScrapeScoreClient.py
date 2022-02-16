import unittest
import sys 

sys.path.append('..')

from CrawlScrapeScoreService import CrawlScrapeScoreService

class CrawlScrapeScoreServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = CrawlScrapeScoreService()

    def test_run(self):
        self.service.run()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()