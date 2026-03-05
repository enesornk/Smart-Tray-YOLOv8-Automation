# 🍽️ Akıllı Tepsi: Derin Öğrenme Tabanlı Yemekhane Otomasyonu

*[Click here for the English version](README.md)*

## 📌 Proje Özeti
Bu proje, üniversite yemekhaneleri ve restoranlar gibi toplu yemek tüketilen alanlarda kasa kuyruklarını azaltmak için geliştirilmiş, görüntü işleme tabanlı otonom bir hesaplama ve besin takip sistemidir.

## 🚀 Problem ve Çözüm
* **Problem:** Geleneksel kasa işlemlerinde kasiyerin ürünleri tek tek girmesi ortalama 30-40 saniye sürmekte ve yoğun saatlerde ciddi darboğazlar yaratmaktadır.
* **Çözüm:** Özel olarak eğitilmiş YOLOv8 modeli sayesinde tepsideki birden fazla ürün aynı anda tespit edilir. Sistem, backend ile haberleşerek toplam fiyat ve kalori hesabını **3-5 saniye** içinde ekrana yansıtır.

## 🛠️ Kullanılan Teknolojiler
* **Yapay Zeka & Görüntü İşleme:** YOLOv8 (Custom Trained), OpenCV
* **Backend:** Python, Flask
* **Veritabanı:** SQLite 
* **Frontend:** HTML/CSS (Jinja2)

## ⚙️ Temel Özellikler
- **Gerçek Zamanlı Nesne Tespiti:** Hamburger, patates kızartması, içecek ve sos gibi ürünleri farklı açılardan, ışık koşullarından ve kısmi kapanmalardan etkilenmeden başarıyla tanır.
- **İlişkisel Mantık ve Fiyatlandırma:** Tespit edilen nesneleri arka plandaki menü sözlüğü ile eşleştirerek anında sepet tutarını hesaplar.
- **Besin Analizi:** Seçilen yemeğin toplam kalori değerini kullanıcıya anlık olarak gösterir.
- **Veritabanı Entegrasyonu:** Tamamlanan her sipariş, silme ve sıfırlama (CRUD) işlemlerini destekleyen SQLite veritabanına dinamik olarak kaydedilir.

## 📥 Kurulum ve Kullanım

1. **Repoyu klonlayın:**
   ```bash
   git clone [https://github.com/enesornk/Smart-Tray-YOLOv8-Automation.git](https://github.com/enesornk/Smart-Tray-YOLOv8-Automation.git)
2. **Gerekli kütüphaneleri kurun:**
   ```bash
   pip install -r requirements.txt
3. **Uygulamayı çalıştırın:**
   ```bash
   python app.py
4. **Tarayıcınızda http://127.0.0.1:5000 adresine giderek arayüze ulaşabilirsiniz.**

## 📄 Dokümantasyon
Modelin eğitim süreci, veri seti oluşturma adımları ve mimari kararlar hakkında daha detaylı bilgi içeren akademik makale formatındaki proje raporuna ve sunum dosyalarına docs/ klasöründen ulaşabilirsiniz.
