import streamlit as st
import requests
import datetime
import requests
import datetime

import streamlit_authenticator as stauth
from pathlib import Path

st.set_page_config(page_title="Journey Mancing", page_icon="🎣", layout="wide")

# ----- USER AUTHENTICATION
names = ["admin", "Feryadi Yulius","Gymnastiar Al Khoarizmy", "Natasya Ega Lina Marbun", "Khusnun Nisa"]
usernames = ["admin", "feryadi", "jimnas", "natee", "khusnun"]
passwords = ["admin", "data", "data", "data", "data"]

credentials = {"usernames":{}}

for un, name, pw in zip(usernames, names, passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})

authenticator = stauth.Authenticate(credentials, "data_mancing", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password salah")
if authentication_status == None:
    st.warning("Masukan Username dan Password")

if authentication_status:

    # Function to get latitude and longitude using Bing Maps API
    def get_coordinates(location):
        bing_maps_api_key = "Ag3lpNHBmRK6m0_yR0F-0IkUghCAglU5Yl4x8a0oJbkCoCB6-4Ha_UQelLt7C6SK"  # Replace with your Bing Maps API key
        url = f"https://dev.virtualearth.net/REST/v1/Locations?q={location}&key={bing_maps_api_key}"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data.get('resourceSets'):
            coordinates = data['resourceSets'][0]['resources'][0]['point']['coordinates']
            return coordinates  # Return latitude and longitude as [latitude, longitude]
        else:
            return None

    # Function to get weather info from a suitable weather API using latitude and longitude
    def get_weather_info(latitude, longitude):
        # Implement logic to fetch weather info from a weather API using latitude and longitude
        # Use an appropriate weather API (e.g., OpenWeatherMap, WeatherAPI, etc.)
        # Replace the code here with the API call to get weather information

        # Example fake weather data
        fake_weather = {
            "temperature": "25°C",
            "condition": "Sunny",
            "wind_speed": "5 m/s"
        }

        return fake_weather


    # Fungsi untuk verifikasi login
    def verify_login(username, password):
        # Ganti URL dengan URL file txt di GitHub yang berisi username dan password
        url = 'https://raw.githubusercontent.com/strng-fer/tubesalpro/main/user.txt'
        response = requests.get(url)
        credentials = response.text.split('\n')
        
        for cred in credentials:
            if ',' in cred:
                stored_username, stored_password = cred.split(',')
                if username == stored_username and password == stored_password:
                    return True
        
        return False

    # Fungsi untuk menambahkan catatan memancing
    def add_note():
        st.title("Tambah Catatan Mancing")
        
        # Memasukkan foto
        uploaded_file = st.file_uploader("Unggah Foto", type=['jpg', 'png'])

        # Memasukkan detail lokasi
        location_details = st.text_input("Detail Lokasi")

        # Memasukkan lokasi pada map untuk mendapatkan latitude dan longitude
        location = st.text_input("Cari Lokasi")
        if location:
            coordinates = get_coordinates(location)
            if coordinates:
                latitude, longitude = coordinates
                st.write("Latitude:", latitude, "Longitude:", longitude)
        # Memasukkan tanggal dan waktu
        date_time = st.date_input("Tanggal") + st.time_input("Waktu")

        # Memasukkan jenis ikan yang ditangkap
        fish_type = st.text_input("Jenis Ikan yang Ditangkap")

        # Memasukkan metode memancing
        fishing_method = st.text_input("Metode Memancing")

        # Tombol untuk menyimpan catatan memancing
        if st.button("Simpan Catatan"):
            # Simpan catatan memancing ke database atau file
            st.success("Catatan Mancing Disimpan")

            # Mendapatkan info cuaca
            weather_info = get_weather_info(latitude, longitude)
            st.subheader("Info Cuaca")
            st.write(f"Temperatur: {weather_info['temperature']}")
            st.write(f"Kondisi Cuaca: {weather_info['condition']}")
            st.write(f"Kecepatan Angin: {weather_info['wind_speed']}")

    # Fungsi untuk mengedit catatan
    def edit_note():
        st.title("Edit Catatan")
        # Implementasikan logika untuk mengedit catatan di sini

    # Fungsi untuk menghapus catatan
    def delete_note():
        st.title("Hapus Catatan")
        # Implementasikan logika untuk menghapus catatan di sini

    def login_page():
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if verify_login(username, password):
                st.success("Login berhasil!")
                return True  # Kembalikan True jika login berhasil
            else:
                st.error("Username atau password salah")
        
        return False  # Kembalikan False jika login gagal

    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}")

    def main_page():
        st.title("Halaman Utama")
        option = st.selectbox("Pilih Operasi", ["Tambah Catatan", "Edit Catatan", "Hapus Catatan"])

        if option == "Tambah Catatan":
            add_note()
        elif option == "Edit Catatan":
            edit_note()
        elif option == "Hapus Catatan":
            delete_note()

    
    def main():
        main_page()

    if __name__ == "__main__":
        main()
    
