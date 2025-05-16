
# Türkçe Kural Tabanlı Duygu Analizi Sistemi

Bu proje, Türkçe cümlelerdeki olumlu ve olumsuz ifadeleri analiz etmek için **Zemberek NLP kütüphanesi** kullanılarak geliştirilmiş bir **kural tabanlı duygu analiz sistemidir**. Hem tekil cümleler hem de Excel dosyası üzerinden toplu test yapılabilir.

## 📌 Proje Dosyaları

| Dosya Adı                 | Açıklama |
|---------------------------|----------|
| `main.py`                | Ana yürütücü dosya, kullanıcıdan girdi alır ve analiz başlatır. |
| `constants.py`           | Zemberek .jar dosyasının yolu burada tanımlanır. |
| `data_preprocessing.py` | Metin temizleme ve kelime kökleştirme işlevlerini içerir. |
| `sentiment_analysis.py` | Duygu analizi ve model değerlendirme mantığını içerir. |
| `visualization.py`      | Performans metriklerinin görselleştirilmesini sağlar. |
| `pozitif_kelimeler.txt` | Olumlu anlam içeren kelimeler. |
| `negatif_kelimeler.txt` | Olumsuz anlam içeren kelimeler. |
| `esit_verilen.xlsx`     | Test cümleleri ve doğru etiketlerini içeren dosya. |

## ⚙️ Özellikler

- **Zemberek** ile morfolojik analiz ve kök çıkartma
- Türkçe cümlelerde **yüklem (fiil) odaklı duygu değerlendirmesi**
- **Negatif yüklem** tespiti ile ters duygu çarpanı
- Doğruluk, Kesinlik, Anma (Recall) ve F1 Skoru gibi **performans metrikleri**
- Yanlış tahminlerin listelenmesi
- Matplotlib ile **grafiksel sonuç görselleştirme**

## 🚀 Kullanım

### 1. Ortam Hazırlığı

- `zemberek-full.jar` dosyasının yolunu `constants.py` içinden güncelleyin.
- `jpype1`, `pandas`, `matplotlib`, `scikit-learn`, `zemberek-python` gibi paketlerin kurulu olduğundan emin olun.

### 2. Çalıştırma

```bash
python main.py
```

Program, kullanıcıdan cümle alarak gerçek zamanlı duygu analizi yapar. Ardından, `esit_verilen.xlsx` dosyası üzerinden model değerlendirmesi yapılır.

### 3. Örnek Girdi

```
Cümle: Bugün çok güzel bir gün.
🔍 Analiz Sonucu: Pozitif
🔍 Güven Skoru: 0.75
🔍 Yüklem Analizi: {'root': 'olmak', 'is_negative': False, ...}
🔍 Bulunan Özellikler: {'positive_words': ['güzel']}
```

## 📊 Performans Metrikleri

- **Doğruluk**
- **Kesinlik (Precision)**
- **Anma (Recall)**
- **F1 Skoru**

Grafik olarak da sunulur.

## 🧠 Geliştirme Fikirleri

- Cümle içerisindeki duygu yoğunluğunu derecelendirme
- Belirsiz duygu içeren örnekleri tanıma
- Web arayüzü veya API entegrasyonu

## 📌 Not

Bu sistem **sözlük tabanlı** olup, makine öğrenmesi kullanılmadan çalışır. Bu sayede açıklanabilir ve modifiye edilebilir bir mimariye sahiptir.

---

Bu sistem, Türkçe doğal dil işleme ve duygu analizi konularına ilgi duyan araştırmacılar, öğrenciler ve geliştiriciler için güçlü bir örnek teşkil eder.
