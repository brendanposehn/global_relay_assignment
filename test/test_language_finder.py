import unittest
import sys 

sys.path.append('..')

from src.apply_language_model import LanguageFinderModelClient

class SpeechTimingModelTest(unittest.TestCase):

    def setUp(self):
        self.language_model_service = LanguageFinderModelClient()
    
    def test_apply(self):
        self.language_model_service.processMetadata()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()