from pathlib import Path
from pprint import pprint

# noinspection PyUnresolvedReferences
from pyate import combo_basic  # todo this crashes with spaCy 3
# noinspection PyPackageRequirements
import RAKE
import spacy
from stop_words import get_stop_words
import yaml


# RAKE stands for Rapid Automatic Keyword Extraction. The algorithm itself is described in the
# Text Mining Applications and Theory book by Michael W. Berry.
stop_words = get_stop_words('en')
rake_obj = RAKE.Rake(stop_words=stop_words)

nlp = spacy.load('en_core_web_sm')

config_path = Path('config.yaml')
config = yaml.safe_load(config_path.read_text())

print("Config:")
pprint(config)
