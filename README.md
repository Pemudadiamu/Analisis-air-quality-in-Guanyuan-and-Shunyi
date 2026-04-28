# Air Quality Dashboard — Analisis Polusi PM2.5

Dashboard interaktif berbasis **Streamlit** untuk menganalisis kualitas udara (PM2.5) di stasiun **Guanyuan** dan **Shunyi** periode 2013–2017.

---

## Struktur Proyek

```
Fundamental Analisi/
├── Air-quality-Guanyuan-Shunyi-dataset/   # Dataset mentah yang di gunakan
│   ├── PRSA_Data_Guanyuan_20130301-20170228.csv
│   └── PRSA_Data_Shunyi_20130301-20170228.csv
├── dashboard/
│   ├── dashboard.py                       # Kode utama dashboard Streamlit
│   └── cleaned_df_quality.csv             # Dataset hasil pembersihan
├── Proyek_Analisis_Data.ipynb             # Notebook analisis & eksplorasi data
├── requirements.txt                       # Daftar dependensi Python
└── README.md                              # Dokumentasi proyek (file ini)
└── url.txt
```


## Cara Menjalankan Dashboard

### Instal Dependensi

```bash
pip install -r requirements.txt
```

### Jalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser pada alamat:

```
http://localhost:8501
```

## Fitur Dashboard

### Dashboard Analisis
- **Tren PM2.5 Bulanan** — Perbandingan rata-rata polusi PM2.5 per bulan antara stasiun Guanyuan dan Shunyi menggunakan line chart.
- **Pengaruh Cuaca terhadap PM2.5** — Scatter plot dengan regresi yang menunjukkan korelasi kecepatan angin dan curah hujan terhadap tingkat polusi.
- **Filter Tahun** — Slider interaktif untuk memfilter data berdasarkan rentang tahun.

### Kalkulator PM2.5
- Masukkan nilai PM2.5 dari sensor cuaca untuk mendapatkan evaluasi status kualitas udara secara real-time:

| Nilai PM2.5 | Status                        |
|--------------|------------------------------|
| 0 – 50       | ✅ Baik (Good)               |
| 51 – 100     | ⚠️ Sedang (Moderate)         |
| 101 – 150    | 🟠 Tidak Sehat (Unhealthy)   |
| > 150        | 🔴 Berbahaya (Hazardous)     |

---

## Catatan Penting

- Pastikan file `cleaned_df_quality.csv` berada di dalam folder `dashboard/` sebelum menjalankan dashboard.
- Jalankan perintah `streamlit run dashboard.py` dari dalam direktori `dashboard/`, bukan dari root proyek.
