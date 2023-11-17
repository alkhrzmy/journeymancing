import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import folium

import streamlit as st

def login(username, password):
    # Ganti ini dengan logika autentikasi yang sesuai
    if username == "admin" and password == "pass":
        return True
    else:
        return False

def main():
    st.title("Aplikasi Login")

    # State untuk menyimpan informasi login
    logged_in = st.session_state.get('logged_in', False)

    if not logged_in:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.success("Login berhasil!")
                st.session_state['logged_in'] = True
            else:
                st.error("Username atau password salah")

    else:
        st.title("Halaman Setelah Login")
        st.write("Anda telah berhasil login sebagai admin.")
        # Tambahkan konten halaman setelah login di sini

if __name__ == "__main__":
    main()


    
# Fungsi untuk membuat tabel catatan memancing jika belum ada
def create_table():
    conn = sqlite3.connect('fishing_notes.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS fishing_notes (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  tanggal DATE,
                  lokasi TEXT,
                  jenis_alat TEXT,
                  cuaca TEXT,
                  jumlah_ikan INTEGER,
                  jenis_ikan TEXT,
                  ukuran_ikan FLOAT,
                  berat_ikan FLOAT,
                  latitude FLOAT,
                  longitude FLOAT
              )
              ''')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan catatan memancing ke database
def add_fishing_note(tanggal, lokasi, jenis_alat, cuaca, jumlah_ikan, jenis_ikan, ukuran_ikan, berat_ikan, latitude, longitude):
    conn = sqlite3.connect('fishing_notes.db')
    c = conn.cursor()
    c.execute('''
              INSERT INTO fishing_notes (tanggal, lokasi, jenis_alat, cuaca, jumlah_ikan, jenis_ikan, ukuran_ikan, berat_ikan, latitude, longitude)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              ''', (tanggal, lokasi, jenis_alat, cuaca, jumlah_ikan, jenis_ikan, ukuran_ikan, berat_ikan, latitude, longitude))
    conn.commit()
    conn.close()

# Fungsi untuk menampilkan catatan memancing
def show_fishing_notes():
    conn = sqlite3.connect('fishing_notes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM fishing_notes')
    data = c.fetchall()
    conn.close()
    return data

# Fungsi untuk melakukan analisis sederhana
def perform_analysis():
    conn = sqlite3.connect('fishing_notes.db')
    df = pd.read_sql_query('SELECT * FROM fishing_notes', conn)
    conn.close()

    # Analisis sederhana
    total_ikan = df['jumlah_ikan'].sum()
    rata_rata_ukuran = df['ukuran_ikan'].mean()
    rata_rata_berat = df['berat_ikan'].mean()

    return total_ikan, rata_rata_ukuran, rata_rata_berat

# Membuat tabel jika belum ada
create_table()

#Login page
if login():
    # Judul halaman jika login berhasil
    st.title('Catatan Memancing')
    # Judul halaman
    st.title('Catatan Memancing')
    
    # Formulir untuk menambahkan catatan memancing
    st.header('Tambah Catatan Memancing')
    tanggal = st.date_input('Tanggal')
    lokasi = st.text_input('Lokasi')
    jenis_alat = st.text_input('Jenis Alat')
    cuaca = st.text_input('Cuaca')
    jumlah_ikan = st.number_input('Jumlah Ikan', min_value=0, step=1)
    jenis_ikan = st.text_input('Jenis Ikan')
    ukuran_ikan = st.number_input('Ukuran Ikan (cm)', min_value=0.0)
    berat_ikan = st.number_input('Berat Ikan (kg)', min_value=0.0)
    latitude = st.number_input('Latitude')
    longitude = st.number_input('Longitude')
    if st.button('Tambah Catatan'):
        add_fishing_note(tanggal, lokasi, jenis_alat, cuaca, jumlah_ikan, jenis_ikan, ukuran_ikan, berat_ikan, latitude, longitude)
        st.success('Catatan berhasil ditambahkan!')
    
    # Menampilkan catatan memancing
    st.header('Catatan Memancing')
    catatan_memancing = show_fishing_notes()
    if catatan_memancing:
        for catatan in catatan_memancing:
            st.write(f"**Tanggal:** {catatan[1]}, **Lokasi:** {catatan[2]}, **Jenis Alat:** {catatan[3]}, **Cuaca:** {catatan[4]}, **Jumlah Ikan:** {catatan[5]}, **Jenis Ikan:** {catatan[6]}, **Ukuran Ikan:** {catatan[7]} cm, **Berat Ikan:** {catatan[8]} kg")
    else:
        st.warning('Belum ada catatan memancing.')
    
    # Menampilkan peta dengan lokasi catatan memancing
    st.header('Peta Lokasi Memancing')
    if catatan_memancing:
        m = folium.Map(location=[catatan_memancing[0][-2], catatan_memancing[0][-1]], zoom_start=10)
        for catatan in catatan_memancing:
            folium.Marker([catatan[-2], catatan[-1]], popup=f"Lokasi: {catatan[2]}", tooltip="Klik untuk info lebih lanjut").add_to(m)
        st.folium_chart(m)
    
    # Analisis sederhana
    st.header('Analisis Sederhana')
    total_ikan, rata_rata_ukuran, rata_rata_berat = perform_analysis()
    st.write(f"Total Ikan yang ditangkap: {total_ikan}")
    st.write(f"Rata-rata Ukuran Ikan: {rata_rata_ukuran:.2f} cm")
    st.write(f"Rata-rata Berat Ikan: {rata_rata_berat:.2f} kg")
else:
    st.stop()
