# Mengimport library yang diperlukan
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker


sns.set(style='dark')

# Membuat fungsi untuk pemrosesan data

# Fungsi untuk menganalisis pola peminjaman berdasarkan musim
def create_seasonal_rentals_df(df):
    seasonal_rentals_df = df.groupby("season").agg({
        "cnt": "sum"
    }).reset_index()
    return seasonal_rentals_df

# Fungsi untuk tren peminjaman berdasarkan jam dalam sehari
def create_hourly_rentals_df(df):
    hourly_rentals_df = df.groupby("hr").agg({
        "cnt": "sum"
    }).reset_index()
    return hourly_rentals_df

# Fungsi untuk pengaruh cuaca terhadap peminjaman
def create_weather_rentals_df(df):
    weather_rentals_df = df.groupby("weathersit").agg({
        "cnt": "sum"
    }).reset_index()
    return weather_rentals_df

# Menentukan path dataset
BASE_DIR = r"E:\.KULIAH USB YPKP\LASKAR AI\Submission\Proyek Akhir Analisis Data"
DAYS_PATH = os.path.join(BASE_DIR, "days_df_clean.csv")
HOURS_PATH = os.path.join(BASE_DIR, "hours_df_clean.csv")

# Memuat dataset
if not os.path.exists(DAYS_PATH) or not os.path.exists(HOURS_PATH):
    st.error("❌ File dataset tidak ditemukan! Pastikan path file sudah benar.")
    st.stop()

days_df = pd.read_csv(DAYS_PATH)
hours_df = pd.read_csv(HOURS_PATH)

# Mengubah tipe data datetime
days_df["dteday"] = pd.to_datetime(days_df["dteday"])
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

# Menampilkan logo 
st.sidebar.image("https://i.pinimg.com/736x/c6/50/f4/c650f4e5ccd180f4939787d899e17ecd.jpg", width=150)

# Sidebar: Menambahkan filter
st.sidebar.header("Filter Data")
season_filter = st.sidebar.multiselect("Pilih Musim:", days_df["season"].unique())

# Filter berdasarkan musim
filtered_df = days_df[days_df["season"].isin(season_filter)] if season_filter else days_df


# Memproses data menggunakan fungsi
seasonal_rentals_df = create_seasonal_rentals_df(filtered_df)
hourly_rentals_df = create_hourly_rentals_df(hours_df)
weather_rentals_df = create_weather_rentals_df(filtered_df)

# Menampilkan Dashboard
st.title("📊 Dashboard Analisis Data Bike Sharing")

## Total Peminjaman Sepeda Berdasarkan Musim
st.subheader("🚴‍♂️ Total Peminjaman Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="season", y="cnt", data=seasonal_rentals_df, ax=ax, estimator=sum)

# Tambahkan label
ax.set_xlabel("Musim")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Total Peminjaman Sepeda Berdasarkan Musim")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: int(x)))

# Tampilkan plot
st.pyplot(fig)

## Tren Peminjaman Sepeda berdasarkan Jam
st.subheader("🕒 Tren Peminjaman Sepeda Berdasarkan Jam")
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(x="hr", y="cnt", data=hourly_rentals_df, ax=ax, marker="o")

# Tambahkan label
ax.set_xlabel("Jam")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Tren Peminjaman Sepeda Berdasarkan Jam")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: int(x)))


# Tampilkan plot
st.pyplot(fig)

## Pengaruh Cuaca terhadap Peminjaman
st.subheader("🌤️ Pengaruh Cuaca terhadap Jumlah Peminjaman")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x="weathersit", y="cnt", data=weather_rentals_df, ax=ax, estimator=sum)  # Tambahkan estimator=sum

# Tambahkan label
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Pengaruh Cuaca terhadap Peminjaman")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: int(x)))

# Tampilkan plot
st.pyplot(fig)

st.caption('Copyright (c) nbl 2025')
