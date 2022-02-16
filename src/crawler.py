from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
from urllib.request import Request, urlopen
import os 

class WAVCrawler:
    '''
        Class used for crawling and scrubbing data from: https://www.voiptroubleshooter.com/open_speech/index.html

        Attributes:
            _base_url: url to crawl and scrub through
            _headers: used for analyzing web pages
            _language_sub_pages: list containing all possible language headers findable at _base_url
            _data_path: path to the data folder where output file is stored
    '''

    _base_url = 'https://www.voiptroubleshooter.com/open_speech/' 
    _headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
    _language_sub_pages = ['American English', 'British English', 'Chinese - Mandarin', 'French', 'Hindi', 'Spanish', 'German']
    _data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data')

    def __init__(self):
        self._urls = []

    def _produceURLs(self):
        '''
            Crawls through site to populate _urls such that all language sub-pages can be linked to.
            All output _url entries in form: 'open_speech/<language>.html
        '''
        f = requests.get(WAVCrawler._base_url, headers = WAVCrawler._headers)
        soup = BeautifulSoup(f.content, 'lxml')
        url_text = soup.get_text().splitlines()
        lines = soup.find_all('a')
        for line in lines:
            for language_page in WAVCrawler._language_sub_pages:
                if language_page in line:
                    line_str = str(line)
                    quote_occurences = [i for i, letter in enumerate(line_str) if letter == '"']
                    url = line_str[quote_occurences[0]+1:quote_occurences[1]]
                    if("open_speech" in url):
                        url = url[3:]
                    else:
                        url = "open_speech/" + url
                    self._urls.append(url)

    def _handleWAVs(self, url):
        '''
            For each inputted url (which is a sub-page from the main site), saves all .wav files
            and appends to/initializes metadata.csv with the metadata from each .wav.
        '''
        language_url = WAVCrawler._base_url[:-12] + url
        f = requests.get(language_url, headers = WAVCrawler._headers)
        wav_list = []
        soup = BeautifulSoup(f.content, 'lxml')
        url_text = soup.get_text().splitlines()
        file_names = []

        if(os.path.isfile(os.path.join(WAVCrawler._data_path, 'metadata.csv'))):
            prev_wav_df = pd.read_csv(os.path.join(WAVCrawler._data_path, 'metadata.csv'))
            file_names = prev_wav_df['File'].values.tolist()
        else:
            prev_wav_df = pd.DataFrame(columns=['File', 'M/F', 'Format', 'Sample Rate', 'Description'])
        
        if('india' in language_url):
            language_url = language_url.replace('india', 'hindi') # TODO get non-hardcoded solution
        
        for i in range(0, len(url_text)):
            if(".wav" in url_text[i]):
                if(url_text[i] in file_names):
                    continue # if more .wavs have been added to the site we still catch them

                wav_url = language_url[:-5] + "/" + url_text[i]
                req = Request(wav_url, headers = WAVCrawler._headers)
                page = urlopen(req)

                with page as f:
                    with open(os.path.join(WAVCrawler._data_path, 'wavs', url_text[i]), 'wb') as f2:
                        f2.write(f.read())
                        
                wav_list.append([url_text[i], url_text[i+1], url_text[i+2], url_text[i+3], url_text[i+4]])
        
        if(len(wav_list) != 0):
            wav_df = pd.DataFrame(wav_list, columns=['File', 'M/F', 'Format', 'Sample Rate', 'Description'])
            wav_df = pd.concat([wav_df, prev_wav_df], ignore_index=True)
            wav_df.to_csv(os.path.join(WAVCrawler._data_path, 'metadata.csv'), index=False)

    def produceMetaData(self):
        '''
            API call to produce metadata.csv and store all .wav files on https://www.voiptroubleshooter.com/open_speech/index.html
        '''
        self._produceURLs()
        for url in self._urls:
            self._handleWAVs(url)
