import torch
import pandas as pd
from IPython.display import Audio
from pprint import pprint
import os

class LanguageFinderModelClient:

    _model, _utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                model='silero_lang_detector',
                                force_reload=False)
    _data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data')
    _sampling_rate = 16000

    def processMetadata(self):
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
