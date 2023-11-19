import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Buat koneksi ke database
engine = create_engine('mysql+mysqlconnector://username:password@host/database')

# Fungsi untuk verifikasi login
def verify_login(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    df = pd.read_sql(query, engine)
    return not df.empty

# Halaman login Streamlit
def login_page():
    st.title("Journey Mancing")
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://example.com/background_image.jpg');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_login(username, password):
            st.success("Login successful!")
            # Redirect ke halaman berikutnya atau lakukan tindakan setelah login berhasil
            # Misalnya:
            # st.write("Lanjut ke halaman berikutnya")
        else:
            st.error("Username atau password salah")

if __name__ == "__main__":
    login_page()
