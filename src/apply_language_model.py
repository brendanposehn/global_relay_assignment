import torch
import pandas as pd
from IPython.display import Audio
from pprint import pprint
import os


class LanguageFinderModelClient:
    '''
        Class used for applying the silero_lang_detector model to .wav data.
        Requires metadata.csv file exist as generated by WAVCrawler.produceMetadata() call

        Attributes:
            _model: the silero_lang_model
            _utils: structure containing utility functions for applying _model
            _data_path: path to the data folder where metadata.csv is stored
    '''

    _model, _utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                model='silero_lang_detector',
                                force_reload=False)
    _data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data')


    def processMetadata(self):
        '''
            Applies silero_lang_detector to .wav files pointed to in metadata.csv,
            and generates a new csv by appending a language colummn onto metadata.csv
            and storing it as language_output.csv
         '''
        get_language, read_audio, *_ = LanguageFinderModelClient._utils
        metadata_df = pd.read_csv(os.path.join(LanguageFinderModelClient._data_path, "metadata.csv"))
        total_rows = metadata_df.shape[0]
        languages = []
        for i in range(0, total_rows):
            file_example = os.path.join(LanguageFinderModelClient._data_path, 'wavs', metadata_df.at[i, 'File'])
            try:
                wav = read_audio(file_example)
            except:
                languages.append("ERROR")
                continue
            language = get_language(wav, LanguageFinderModelClient._model)
            languages.append(language)

        metadata_df['Language'] = languages
        metadata_df.to_csv(os.path.join(LanguageFinderModelClient._data_path, "language_output.csv"), index=False)
