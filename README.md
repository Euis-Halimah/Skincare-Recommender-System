# Skincare Recommender System

Sistem rekomendasi skincare ini dikembangkan melalui beberapa tahapan pengolahan data dan pemodelan sebagai berikut:

## 🔍 1. Scraping Data
Langkah pertama adalah **scraping data** menggunakan Selenium.  
- File scraping: disimpan dalam folder: `selenium-scraping/`
- Hasil scraping disimpan di folder: `dataset/`

## 📊 2. Statistika Deskriptif
File `statistika_deskriptif.ipynb` digunakan untuk:
- Menyatukan seluruh file `.csv` hasil scraping menjadi satu file yaitu `skincaret.csv
- Melakukan analisis deskriptif awal terhadap data

## 🧼 3. Preprocessing Tahap 1: Kolom Benefit
- File: `preprocessing_skincare.ipynb`
- Proses: Membersihkan dan mengekstrak kolom *benefit*
- Output: `hasil_preprocessing_benefit.csv`

## 🧪 4. Preprocessing Tahap 2: Ingredients
- File: `preprocessing_teks_lanjutan_skincare.ipynb`
- Input: `hasil_preprocessing_benefit.csv`
- Output akhir: `data_cleaned.xlsx`, yaitu dataset siap pakai untuk model rekomendasi

## 🤖 5. Recommender System
- File utama: `recommender_system.ipynb`
- Menggunakan data dari `data_cleaned.xlsx` untuk membangun sistem rekomendasi skincare

## 🛠 6. Class Function & Model Training
- Kode class model: `model_recommender.py`
- Menyimpan model terlatih ke file: `model_rekomendasi.pkl` menggunakan: `save_model.py`

## 💻 7. Deploy Sistem dengan Gradio
- File: `app.py`
- Mengembangkan antarmuka sistem rekomendasi menggunakan Gradio
- open terminal dan jalankan python app.py

---

