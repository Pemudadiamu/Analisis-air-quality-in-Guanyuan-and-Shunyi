import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Dashboard Air Quality",  layout="wide")

st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif !important;
        }
        
        .block-container {
            padding-top: 2rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "cleaned_df_quality.csv")

    df = pd.read_csv(file_path)
    df['datatime'] = pd.to_datetime(df['datatime'])
    return df

df_all = load_data()


with st.sidebar:
    st.markdown('<h2 class="text-2xl font-bold text-gray-800 mb-4">Main Menu </h2>', unsafe_allow_html=True)
    pilihan_menu = st.radio("Pilih Halaman:", ["Dashboard Analisis", "Kalkulator PM2.5"])
    st.markdown('<hr class="my-4 border-gray-300">', unsafe_allow_html=True)


# memfilter dataset 
if pilihan_menu == "Dashboard Analisis":
    
    st.markdown("""
        <div class="bg-yellow-400 p-8 rounded-lg shadow-lg mb-6 mt-6 text-white">
            <h1 class="text-3xl font-bold mb-2"> Air Quality Dashboard</h1>
            <p class="text-blue-100 text-lg">Analisis Polusi Udara PM2.5 di Stasiun Guanyuan & Shunyi (2013-2017)</p>
        </div>
    """, unsafe_allow_html=True)
    with st.sidebar:
            st.markdown('<h3 class="text-xl font-bold text-gray-800 mb-2">Filter Data</h3>', unsafe_allow_html=True)
            min_year = int(df_all['datatime'].dt.year.min())
            max_year = int(df_all['datatime'].dt.year.max())
            selected_year = st.slider("Pilih Rentang Tahun", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    main_df = df_all[(df_all['datatime'].dt.year >= selected_year[0]) & (df_all['datatime'].dt.year <= selected_year[1])]

    # Visualisasi 1: Pertanyaan Bisnis 1
    st.markdown('<h3 class="text-2xl font-bold text-gray-800 mt-8 mb-4"> Tren PM2.5 Bulanan (Guanyuan vs Shunyi)</h3>', unsafe_allow_html=True)
    monthly_pm25 = main_df.groupby([main_df['datatime'].dt.month, 'station'])['PM2.5'].mean().reset_index()
    monthly_pm25.rename(columns={'datatime': 'month'}, inplace=True)

    fig_line, ax_line = plt.subplots(figsize=(12, 5))
    sns.lineplot(
        data=monthly_pm25, x='month', y='PM2.5', hue='station', 
        marker='o', linewidth=2.5, palette=['#ef4444', '#3b82f6'], ax=ax_line
    )
    ax_line.set_xlabel('Bulan', fontsize=12)
    ax_line.set_ylabel('Rata-Rata PM2.5 (µg/m³)', fontsize=12)
    ax_line.set_xticks(range(1, 13))
    ax_line.set_xticklabels(['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'])
    ax_line.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig_line)

    with st.expander("Lihat Penjelasan Tren"):
        st.write("Polusi terburuk secara konsisten terjadi pada musim dingin (Desember - Januari), sedangkan kualitas udara terbaik berada di bulan Agustus. Stasiun Guanyuan mencatat dengan konsisten rata-rata polusi yang lebih tinggi dibandingkan Shunyi.")

    # Visualisasi 2:  Pertanyaan Bisnis 2
    st.markdown('<h3 class="text-2xl font-bold text-gray-800 mt-10 mb-4"> Pengaruh Cuaca terhadap Polusi PM2.5</h3>', unsafe_allow_html=True)

    # Mengambil sample agar visualisasi scatter plot ringan saat di-render
    sample_df = main_df.sample(n=3000, random_state=42)

    col1, col2 = st.columns(2)

    with col1:
        fig_scatter1, ax_scatter1 = plt.subplots(figsize=(8, 6))
        sns.regplot(
            data=sample_df, x='WSPM', y='PM2.5', 
            scatter_kws={'alpha': 0.3, 'color': '#0ea5e9'}, line_kws={'color': '#ef4444', 'linewidth': 2}, ax=ax_scatter1
        )
        ax_scatter1.set_title('Kecepatan Angin vs PM2.5', fontsize=14, fontweight='bold')
        ax_scatter1.set_xlabel('Kecepatan Angin (m/s)')
        st.pyplot(fig_scatter1)

    with col2:
        fig_scatter2, ax_scatter2 = plt.subplots(figsize=(8, 6))
        sns.regplot(
            data=sample_df, x='RAIN', y='PM2.5', 
            scatter_kws={'alpha': 0.3, 'color': '#10b981'}, line_kws={'color': '#ef4444', 'linewidth': 2}, ax=ax_scatter2
        )
        ax_scatter2.set_title('Curah Hujan vs PM2.5', fontsize=14, fontweight='bold')
        ax_scatter2.set_xlabel('Curah Hujan (mm)')
        st.pyplot(fig_scatter2)

    with st.expander("Lihat Penjelasan Korelasi"):
        st.write("Kecepatan angin memiliki korelasi negatif yang cukup kuat terhadap polusi, angin kencang terbukti efektif menyapu PM2.5. Di sisi lain, curah hujan secara observasi per jam tidak menunjukkan dampak signifikan dalam menurunkan tingkat polusi.")

elif pilihan_menu == "Kalkulator PM2.5":
    
    st.markdown("""
        <div class="bg-indigo-600 p-6 rounded-lg shadow-lg mb-6 mt-6 text-white">
            <h1 class="text-3xl font-bold mb-2">Kalkulator Status Kualitas Udara</h1>
            <p class="text-indigo-100 text-lg">Prediksi tingkat bahaya polusi udara secara real-time berdasarkan angka PM2.5</p>
        </div>
    """, unsafe_allow_html=True)

    col_input, col_result = st.columns([1, 2])

    with col_input:
        st.markdown('<div class="bg-white p-4 rounded-lg shadow border border-gray-200 text-black"> Input Nilai PM2.5', unsafe_allow_html=True)
        pm25_input = st.number_input(label= "", min_value=0.0, max_value=1000.0, value=45.0, step=1.0)
        cek_button = st.button("Cek Status Sekarang", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        if cek_button:
            if pm25_input <= 50:
                status, bg_color= "Baik (Good)", "bg-green-500"
                rekomendasi = "Kualitas udara sangat sehat. Sangat ideal untuk berolahraga dan aktivitas penuh di luar ruangan!"
            elif pm25_input <= 100:
                status, bg_color= "Sedang (Moderate)", "bg-yellow-500"
                rekomendasi = "Kualitas udara dapat diterima. Namun, kelompok sensitif (asma/alergi) sebaiknya membatasi aktivitas berat di luar."
            elif pm25_input <= 150:
                status, bg_color= "Tidak Sehat (Unhealthy)", "bg-orange-500"
                rekomendasi = "Masyarakat umum mulai merasakan dampak kesehatan. Sangat disarankan memakai masker jika keluar rumah."
            else:
                status, bg_color= "Berbahaya (Hazardous)", "bg-red-600"
                rekomendasi = "PERINGATAN DARURAT! Tingkat polusi ekstrem. Hindari seluruh aktivitas luar ruangan dan segera nyalakan air purifier."

            st.markdown(f"""
                <div class="{bg_color} p-6 rounded-xl shadow-md text-white transition-all duration-500 border-2 border-white">
                    <h4 class="font-bold text-3xl mb-3"> Status: {status}</h4>
                    <p class="text-xl"><strong>Rekomendasi Sistem:</strong> <br>{rekomendasi}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Masukkan angka dari sensor cuaca di samping dan klik tombol untuk melihat hasil evaluasi.")