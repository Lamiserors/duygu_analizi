from collections import defaultdict
from zemberek.tokenization import TurkishTokenizer
from sklearn.feature_extraction.text import CountVectorizer

from data_preprocessing import preprocess_text

def analyze_sentiment(sentence, 
                      morphology, 
                      positive_dict, 
                      negative_dict):
    """
    Verilen bir cümlenin duygu analizini yapar (optimize edilmiş).
    """
    try:
        sentence = preprocess_text(sentence)
        raw_tokens = TurkishTokenizer.DEFAULT.tokenize(sentence)
        tokens = [t.content.lower() for t in raw_tokens if t.content.strip() != '']
        # predicate_multiplier = -1 if 'kadar' in tokens else 1
        # Morfolojik analiz bir kez yapılır
        results = morphology.analyze_and_disambiguate(" ".join(tokens)).best_analysis()
        predicate_multiplier =1
        # Yüklem analizi (Verb ve Neg kontrolü)
        predicate_info = None
        for analysis in reversed(results):
            morphemes = str(analysis)
            if 'Verb' in morphemes:
                has_negation = 'Neg' in morphemes
                predicate_info = {
                    'root': analysis.item.root,
                    'is_negative': has_negation,
                    'full_analysis': str(analysis)
                }
                predicate_multiplier = -1*predicate_multiplier if has_negation else 1*predicate_multiplier
                break

        score = 0
        confidence = 0
        found_features = defaultdict(list)

        # Predicate bilgisi eklenir
        if predicate_info:
            found_features['predicate'] = [{
                'root': predicate_info['root'],
                'is_negative': predicate_info['is_negative'],
                'analysis': predicate_info['full_analysis']
            }]

        # Kelime analizleri
        for result in results:
            root = result.item.root or result.item.normalized_form
            root = root.lower() if root else ""
            if root in positive_dict:
                score += positive_dict[root] * predicate_multiplier
                confidence += 1
                found_features['positive_words'].append(root)
            elif root in negative_dict:
                score += negative_dict[root] * predicate_multiplier * -1
                confidence += 1
                found_features['negative_words'].append(root)

            # if root == "kadar":
            #     score = score * -1

    
        # Güven skoru hesaplanır
        confidence_score = confidence / len(tokens) if tokens else 0
        sentiment = "Pozitif" if score > 0 else "Negatif"

        return {
            'sentiment': sentiment,
            'score': score,
            'confidence': confidence_score,
            'features': dict(found_features),
            'predicate_analysis': predicate_info
        }
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return {
            'sentiment': "Hata",
            'score': 0,
            'confidence': 0,
            'features': {},
            'predicate_analysis': None
        }

def evaluate_model(test_data, 
                   morphology, 
                   positive_dict, 
                   negative_dict):
    """
    Test verisini kullanarak modeli değerlendirir (optimize edilmiş).
    """
    results = {'DP': 0, 'DN': 0, 'YP': 0, 'YN': 0, 'predictions': [], 'wrong_predictions': []}
    for sentence, true_label in test_data:
        analysis = analyze_sentiment(sentence, morphology, positive_dict, negative_dict)
        prediction = analysis['sentiment']

        if prediction == "Pozitif" and true_label == "Pozitif":
            results['DP'] += 1
        elif prediction == "Negatif" and true_label == "Negatif":
            results['DN'] += 1
        elif prediction == "Pozitif" and true_label == "Negatif":
            results['YP'] += 1
            results['wrong_predictions'].append({
                'text': sentence,
                'true_label': true_label,
                'predicted': prediction,
                'confidence': analysis['confidence']
            })
        elif prediction == "Negatif" and true_label == "Pozitif":
            results['YN'] += 1
            results['wrong_predictions'].append({
                'text': sentence,
                'true_label': true_label,
                'predicted': prediction,
                'confidence': analysis['confidence']
            })

        results['predictions'].append({
            'text': sentence,
            'true_label': true_label,
            'predicted': prediction,
            'confidence': analysis['confidence'],
            'features': analysis['features']
        })
    return results
