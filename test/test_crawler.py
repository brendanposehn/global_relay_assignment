import unittest
import sys 

sys.path.append('..')

from src.crawler import WAVCrawler

class WAVCrawlerTest(unittest.TestCase):

    def setUp(self):
        self.crawler = WAVCrawler()

    def test_produceURLs(self):
        self.crawler._produceURLs()
        self.assertEqual(len(self.crawler._urls), 5) # would change if Spanish and/or German added
        for url in self.crawler._urls:
            self.assertTrue('html' in url)
            self.assertTrue('open_speech/' in url)

    def test_handleWAVS(self):
        self.crawler._produceURLs()
        for url in self.crawler._urls:
            self.crawler._handleWAVs(url)
        self.assertTrue(True) # TODO add more in-depth check 

if __name__ == '__main__':
    unittest.main()