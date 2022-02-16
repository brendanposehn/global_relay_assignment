import torch
import pandas as pd
from IPython.display import Audio
from pprint import pprint
import os

class ModelApplicantBase:

    def __init__(self, model_repo, model_name):
        self._model, self._utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                            model='silero_lang_detector',
                            force_reload=True) #can this be false?

    def processMetadata(self):
        raise NotImplementedError('You need to define a speak method!')

    def processOutput(self):
        raise NotImplementedError('You need to define a speak method!')