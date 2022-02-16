from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
from urllib.request import Request, urlopen
import os 

class WAVCrawler:

    _base_url = 'https://www.voiptroubleshooter.com/open_speech/' 
    _headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    _language_sub_pages = ['American English', 'British English', 'Chinese - Mandarin', 'French', 'Hindi', 'Spanish', 'German']
    _urls = []

    @staticmethod
    def _findCharOccurrences(s, ch):
        return [i for i, letter in enumerate(s) if letter == ch]

    def _produceURLs(self):
        f = requests.get(_base_url, headers = _headers)
        soup = BeautifulSoup(f.content, 'lxml')
        url_text = soup.get_text().splitlines()
        lines = soup.find_all('a')
        for line in lines:
            for language_page in _language_sub_pages:
                if language_page in line:
                    line_str = str(line)
                    quote_occurences = findCharOccurrences(line_str, '"')
                    url = line_str[quote_occurences[0]+1:quote_occurences[1]]
                    if("open_speech" in url):
                        url = url[3:]
                    else:
                        url = "open_speech/" + url
                    _urls.append(url)


    def _handleWAVs(self, url):
        f = requests.get(language_url, headers = headers)
        wav_list = []
        soup = BeautifulSoup(f.content, 'lxml')
        url_text = soup.get_text().splitlines()
        for i in range(0, len(url_text)):
            if(".wav" in url_text[i]):
                wav_url = language_url[:-5] + "/" + url_text[i]
                req = Request(wav_url, headers = headers)
                page = urlopen(req)
                with page as f: # TODO make paths relative
                    open(os.path.join('C:/Users/brend/Desktop/global_relay_docker/data/', url_text[i]), 'wb').write(f.read())
                wav_list.append([url_text[i], url_text[i+1], url_text[i+2], url_text[i+3], url_text[i+4], " "])

        wav_df = pd.DataFrame(wav_list, columns=['File', 'M/F', 'Format', 'Sample Rate', 'Description', 'has_speech'])
        wav_df.to_csv('C:/Users/brend/Desktop/global_relay_docker/data/metadata.csv', index=False) # TODO make paths relative 
