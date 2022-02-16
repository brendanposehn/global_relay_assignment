import unittest
import sys 

sys.path.append('..')

from src.apply_speech_timing_model import SpeechTimingModelClient

class SpeechTimingModelTest(unittest.TestCase):

    def setUp(self):
        self.speech_model_service = SpeechTimingModelClient()
    
    def test_apply(self):
        self.speech_model_service.processMetadata()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()