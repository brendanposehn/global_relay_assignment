import torch
import pandas as pd
from IPython.display import Audio
from pprint import pprint
import os

class SpeechTimingModelClient:

    _model, _utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=False)
    _data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data')
    _sampling_rate = 16000

    def processMetadata(self):
        (get_speech_timestamps, _, read_audio, *_) = SpeechTimingModelClient._utils
        metadata_df = pd.read_csv(os.path.join(SpeechTimingModelClient._data_path, "metadata.csv"))
        total_rows = metadata_df.shape[0]
        has_speech_list = []
        start_list = []
        end_list = []
        for i in range(0, total_rows):
            file_example = os.path.join(SpeechTimingModelClient._data_path, 'wavs', metadata_df.at[i, 'File'])
            try:
                wav = read_audio(file_example, sampling_rate=SpeechTimingModelClient._sampling_rate)
            except:
                has_speech_list.append('ERROR')
                start_list.append('ERROR')
                end_list.append('ERROR')
                continue

            speech_timestamps = get_speech_timestamps(wav, SpeechTimingModelClient._model, sampling_rate=SpeechTimingModelClient._sampling_rate)
            if(not speech_timestamps):
                has_speech_list.append('false')
                start_list.append('')
                end_list.append('')
                continue

            starts = ""
            ends = ""
            for pair in speech_timestamps:
                starts += str(pair['start']) + ":"
                ends += str(pair['end']) + ":"
            starts = starts[:-1]
            ends = ends[:-1]
            has_speech_list.append('true')
            start_list.append(starts)
            end_list.append(ends)
        metadata_df['has_speech'] = has_speech_list
        metadata_df['speech_starts'] = start_list
        metadata_df['speech_ends'] = end_list
        metadata_df.to_csv(os.path.join(SpeechTimingModelClient._data_path, "speech_timing_output.csv"), index=False)