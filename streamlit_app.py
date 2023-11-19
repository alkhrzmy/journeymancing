import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Fungsi untuk menghubungkan ke database SQL
def create_connection():
    engine = create_engine('mysql+mysqlconnector://username:password@localhost/nama_database')
    conn = engine.connect()
    return conn

# Fungsi untuk melakukan login
def login(username, password):
    conn = create_connection()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = conn.execute(query)
    return result.fetchone()

# Fungsi untuk tampilan halaman login
def login_page():
    st.title("Journey Mancing")
    st.markdown("## Silakan login untuk melanjutkan")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        user = login(username, password)
        if user:
            st.success("Login berhasil!")
            # Redirect ke halaman selanjutnya setelah login berhasil
            st.write("Halaman selanjutnya...")
        else:
            st.error("Login gagal. Silakan coba lagi.")

# Fungsi untuk tampilan halaman utama
def main_page():
    st.title("Halaman Utama")
    st.markdown("## Selamat datang di Journey Mancing!")
    st.markdown("Silakan login untuk memulai.")

# Logika untuk menampilkan halaman login atau halaman utama berdasarkan status login
is_logged_in = False  # Ganti dengan fungsi cek login yang sesuai
if is_logged_in:
    main_page()
else:
    login_page()
