import streamlit as st
import git
import csv
import requests
import datetime

import streamlit_authenticator as stauth

st.set_page_config(page_title="Journal Mancing", page_icon="🎣", layout="wide")

st.header("Journal Mancing®")

# ----- USER AUTHENTICATION
names = ["admin", "Feryadi Yulius","Gymnastiar Al Khoarizmy", "Natasya Ega Lina Marbun", "Khusnun Nisa"]
usernames = ["admin", "feryadi", "jimnas", "natee", "khusnun"]
passwords = ["admin", "data", "data", "data", "data"]

hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {"usernames":{}}

for un, name, pw in zip(usernames, names, hashed_passwords):
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
        
    # Fungsi untuk menambahkan catatan memancing
    def add_note():
        st.title("Tambah Catatan Mancing")
        
        # Memasukkan foto
        uploaded_file = st.file_uploader("Unggah Foto", type=['jpg', 'png'])
    
        # Memasukkan detail lokasi
        location_details = st.text_input("Detail Lokasi")
    
        # Memasukkan lokasi pada map untuk mendapatkan latitude dan longitude
        location = st.text_input("Cari Lokasi")
        latitude, longitude = None, None  # Initialize to None
        if location:
            coordinates = get_coordinates(location)
            if coordinates:
                latitude, longitude = coordinates
                st.write("Latitude:", latitude, "Longitude:", longitude)
    
        # Input tanggal
        input_date = st.date_input("Tanggal")
    
        # Input waktu
        input_time = st.time_input("Waktu")
    
        # Menggabungkan tanggal dan waktu menjadi objek datetime
        combined_datetime = datetime.datetime.combine(input_date, input_time)
    
        # Memasukkan jenis ikan yang ditangkap
        fish_type = st.text_input("Jenis Ikan yang Ditangkap")
    
        # Memasukkan metode memancing
        fishing_method = st.text_input("Metode Memancing")
    
        # Tombol untuk menyimpan catatan memancing
        if st.button("Simpan Catatan"):
            if latitude is not None and longitude is not None:
                note_data = [combined_datetime, fish_type, fishing_method, location_details]
    
                # Simpan data catatan ke dalam file lokal (catatan_mancing.csv)
                st.success("Catatan Mancing Disimpan")
    
                # Mendapatkan info cuaca jika koordinat telah didapat
                if latitude and longitude:
                    weather_info = get_weather_info(latitude, longitude)
                    st.subheader("Info Cuaca")
                    st.write(f"Temperatur: {weather_info['temperature']}")
                    st.write(f"Kondisi Cuaca: {weather_info['condition']}")
                    st.write(f"Kecepatan Angin: {weather_info['wind_speed']}")
            else:
                st.warning("Harap cari lokasi yang valid untuk mendapatkan informasi cuaca")
    

    # Fungsi untuk mengedit catatan
    def edit_note(index, updated_note):
        pass
        
    # Fungsi untuk menghapus catatan
    def delete_note(index):
        pass


    def tampilkan_catatan():
        pass

        # Sidebar navigation function
    def sidebar_navigation():
        st.sidebar.title("Navigation")
        if st.sidebar.button("Home"):
            return "Home"
        elif st.sidebar.button("Analytics"):
            return "Analytics"
        else:
            return "Home"  # Default to Home if no button is clicked
    
    # Function to display analytics page
    def analytics_page():
        st.title("Analytics Page")
        # Add your analytics content here
        st.write("Analytics content goes here")
        
        authenticator.logout("Logout","sidebar")
        st.sidebar.title(f"Welcome {name}")


    def main_page():
        st.title("Halaman Utama")
    
        button_col1, button_col2, button_col3 = st.columns(3)
        
        if button_col1.button("Tambah Catatan"):
            add_note()
        elif button_col2.button("Edit Catatan"):
            edit_note()
        elif button_col3.button("Hapus Catatan"):
            delete_note()

    def main():
        choice = sidebar_navigation()
        if choice == "Home":
            main_page()
        elif choice == "Analytics":
            analytics_page()

    if __name__ == "__main__":
        main()
    
