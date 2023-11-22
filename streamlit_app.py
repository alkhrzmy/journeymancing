import streamlit as st
import git
import csv
import requests
import datetime
from PIL import Image

import streamlit_authenticator as stauth

import streamlit.components.v1 as components

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
    # HTML template for the location picker
    # Display the location picker
    google_maps_autocomplete = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Google Maps API - Autocomplete Address Search Box with Map Example</title>
        <style type="text/css">
            #map {
                width: 100%;
                height: 400px;
            }
            .mapControls {
                margin-top: 10px;
                border: 1px solid transparent;
                border-radius: 2px 0 0 2px;
                box-sizing: border-box;
                -moz-box-sizing: border-box;
                height: 32px;
                outline: none;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
            }
            #searchMapInput {
                background-color: #fff;
                font-family: Roboto;
                font-size: 15px;
                font-weight: 300;
                margin-left: 12px;
                padding: 0 11px 0 13px;
                text-overflow: ellipsis;
                width: 50%;
                color: #ffffff;
            }
            #searchMapInput:focus {
                border-color: #4d90fe;
            }
            #geoData {
                color: #ffffff; /* Ubah warna font menjadi putih */
            }
        </style>
    </head>
    <body>
    
    <input id="searchMapInput" class="mapControls" type="text" placeholder="Enter a location">
    <div id="map"></div>
    <ul id="geoData">
        <li>Full Address: <span id="location-snap"></span></li>
        <li>Latitude: <span id="lat-span"></span></li>
        <li>Longitude: <span id="lon-span"></span></li>
    </ul>
    
    <script>
    function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -5.3582643, lng: 105.3148495},
        zoom: 13
        });
        var input = document.getElementById('searchMapInput');
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    
        var autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.bindTo('bounds', map);
    
        var infowindow = new google.maps.InfoWindow();
        var marker = new google.maps.Marker({
            map: map,
            anchorPoint: new google.maps.Point(0, -29)
        });

        google.maps.event.addListener(map, 'click', function(event) {
            marker.setVisible(false);
            marker.setPosition(event.latLng);
            marker.setVisible(true);
    
            var clickedLat = event.latLng.lat();
            var clickedLng = event.latLng.lng();
    
            // Tampilkan info di info window
            infowindow.setContent('<div>Clicked Location<br>Latitude: ' + clickedLat + '<br>Longitude: ' + clickedLng);
            infowindow.open(map, marker);
    
            // Simpan koordinat di elemen HTML
            document.getElementById('lat').innerHTML = clickedLat;
            document.getElementById('lon').innerHTML = clickedLng;
            return [lat, lon];
        });
    }
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA6JQDWAVYXN07fZAtBK-ATcBg750J68bQ&libraries=places&callback=initMap" async defer></script>
    </body>
    </html>
    """

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
        if lat is not None and lon is not None:
            note_data = [combined_datetime, fish_type, fishing_method, location_details]

            # Simpan data catatan ke dalam file lokal (catatan_mancing.csv)
            st.success("Catatan Mancing Disimpan")

            # Mendapatkan info cuaca jika koordinat telah didapat
            if latitude and longitude:
                weather_info = get_weather_info(lat, lon)
                st.subheader("Info Cuaca")
                st.write(f"Temperatur: {weather_info['temperature']}")
                st.write(f"Kondisi Cuaca: {weather_info['condition']}")
                st.write(f"Kecepatan Angin: {weather_info['wind_speed']}")
        else:
            st.warning("Harap cari lokasi yang valid untuk mendapatkan informasi cuaca")


# Fungsi untuk mengedit catatan
def edit_note():
    st.write("Journal")


# Fungsi untuk menghapus catatan
def delete_note():
    st.write("Journal")


def tampilkan_catatan():
    st.write("Journal")


# Sidebar navigation function
current_page = "Home"  # Inisialisasi status halaman


def sidebar_navigation():
    st.sidebar.title("Wellcome bro")
    global current_page  # Gunakan variabel global untuk menyimpan status halaman terkini
    if st.sidebar.button("Home"):
        current_page = "Home"
    elif st.sidebar.button("Analytics"):
        current_page = "Analytics"
    return current_page  # Mengembalikan status halaman terkini


# Function to display analytics page
def analytics_page():
    st.title("Analytics Page")
    # Add your analytics content here
    st.write("Analytics content goes here")


def button_coiche():
    button_col1, button_col2, button_col3 = st.tabs(["Tambah Catatan", "Edit Catatan", "Hapus Catatan"])

    with button_col1:
        add_note()
    with button_col2:
        edit_note()
    with button_col3:
        delete_note()

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
    def main_page():
        st.title("Home Page")
        button_coiche()


    def main():
        choice = sidebar_navigation()
        if choice == "Home":
            main_page()
        elif choice == "Analytics":
            analytics_page()
            
    if __name__ == "__main__":
        main()
