import unittest
sys.path.append("..")
from crawler import WAVCrawler

class WAVCrawlerTest(unittest.TestCase):

    def setUp(self):
        self.crawler = WavCrawler()

    def IsTrue(self):
        assert(True)

if __name__ == '__main__':
    unittest.main()