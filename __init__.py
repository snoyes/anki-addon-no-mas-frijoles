import aqt
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from googletrans import Translator

translator = Translator()
t = translator.translate('no mas frijoles')
aqt.utils.showInfo(t.text)
