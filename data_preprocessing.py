# data_preprocessing.py
import re
from zemberek.morphology import TurkishMorphology

def preprocess_text(text):
    """
    Metni küçük harfe çevirir ve özel karakterleri kaldırır
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def preprocess_txt_words(file_path, morphology):
    """
    TXT dosyasındaki kelimeleri köklerine indirger ve bir sözlük oluşturur.
    """
    roots = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    analysis = morphology.analyze_and_disambiguate(word).best_analysis()
                    for result in analysis:
                        root = result.item.root
                        if root:
                            roots.add(root.lower())
        return {root: 1 for root in roots}
    except Exception as e:
        print(f"TXT dosyası işlenirken hata oluştu: {e}")
        return {}
