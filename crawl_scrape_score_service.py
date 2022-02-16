from src.crawler import WAVCrawler
from src.apply_language_model import LanguageFinderModelClient
from src.apply_speech_timing_model import SpeechTimingModelClient

class CrawlScrapeScoreService:

    def run(self):
        crawler = WAVCrawler()
        timing_client = SpeechTimingModelClient()
        language_client = LanguageFinderModelClient()

        crawler.produceMetaData()
        timing_client.processMetadata()
        language_client.processMetadata()     