# constants.py
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
from jpype import startJVM, shutdownJVM, isJVMStarted
from zemberek.morphology import TurkishMorphology
from zemberek.tokenization import TurkishTokenizer
from sklearn.feature_extraction.text import CountVectorizer

# Zemberek kütüphanesi dosya yolu (Kendi sisteminizdeki .jar dosyası yolunu güncelleyin)
ZEMBEREK_PATH = "C:/Users/kenan/Desktop/pythoodev/zemberek-full.jar"

