# main.py
from jpype import startJVM, shutdownJVM, isJVMStarted
from zemberek.morphology import TurkishMorphology
import pandas as pd

# Kendi modüllerimizden import ediyoruz
from constants import ZEMBEREK_PATH
from data_preprocessing import preprocess_txt_words
from sentiment_analysis import analyze_sentiment, evaluate_model
from visualization import plot_performance_metrics

def main():
    try:
        # JVM başlatma
        startJVM("-Djava.class.path=" + ZEMBEREK_PATH)
        morphology = TurkishMorphology.create_with_defaults()
        # pozitif_file="kenan_positif2.txt"
        # negatif_file="kenan_negatif2.txt"
        #TXT dosyalarını köklere indirgeme
        positive_dict = preprocess_txt_words("C:/Users/kenan/Desktop/kural_tabanli_duygu_analizi/pozitif_kelimeler.txt", morphology)
        negative_dict = preprocess_txt_words("C:/Users/kenan/Desktop/kural_tabanli_duygu_analizi/negatif_kelimeler.txt", morphology)

#"C:/Users/kenan/Desktop/piton_proje/xx.txt"
        print("Lütfen analiz etmek istediğiniz cümleleri girin. Çıkmak için 'q' yazın.")
        while True:
            user_input = input("Cümle: ").strip()
            if user_input.lower() == 'q':
                break
            if user_input:
                analysis = analyze_sentiment(
                    sentence=user_input, 
                    morphology=morphology, 
                    positive_dict=positive_dict, 
                    negative_dict=negative_dict, 

                )
                print(f"\n🔍 Cümle: {user_input}")
                print(f"🔍 Analiz Sonucu: {analysis['sentiment']}")
                print(f"🔍 Güven Skoru: {analysis['confidence']:.2f}")
                if analysis['predicate_analysis']:
                    print(f"🔍 Yüklem Analizi: {analysis['predicate_analysis']}")
                print(f"🔍 Bulunan Özellikler: {analysis['features']}")

        
        # Test verilerini yükle ve değerlendirme yap
        df = pd.read_excel("C:/Users/kenan/Desktop/kural_tabanli_duygu_analizi/esit_verilen.xlsx")
        test_data = list(zip(df["Cümle"], df["Sınıf"]))

        results = evaluate_model(
            test_data=test_data, 
            morphology=morphology, 
            positive_dict=positive_dict, 
            negative_dict=negative_dict, 
        )

        toplam = sum(results[k] for k in ['DP', 'DN', 'YP', 'YN'])
        doğruluk = (results['DP'] + results['DN']) / toplam if toplam > 0 else 0
        kesinlik = results['DP'] / (results['DP'] + results['YP']) if (results['DP'] + results['YP']) > 0 else 0
        anma = results['DP'] / (results['DP'] + results['YN']) if (results['DP'] + results['YN']) > 0 else 0
        f1 = (2 * kesinlik * anma) / (kesinlik + anma) if (kesinlik + anma) > 0 else 0

        metrics = {
            "Doğruluk": doğruluk,
            "Kesinlik": kesinlik,
            "Anma": anma,
            "F1 Skoru": f1
        }

        # Performans metriklerini yüzdelik olarak yazdır
        print("\nPerformans Metrikleri (Yüzdelik):")
        for metric, value in metrics.items():
            print(f"{metric}: {value * 100:.2f}%")

        # Performans metriklerini görselleştir
        plot_performance_metrics(metrics)

        # Yanlış tahminleri yazdır
        print("\n🔍 Yanlış Tahminler:")
        for wp in results['wrong_predictions']:
            print(f"  - Cümle: {wp['text']}")
            print(f"    Gerçek Etiket: {wp['true_label']}")
            print(f"    Tahmin: {wp['predicted']}")

    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        if isJVMStarted():
            shutdownJVM()
            print("JVM kapatıldı.")

if __name__ == "__main__":
    main()
