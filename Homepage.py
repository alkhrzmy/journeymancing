import streamlit as st
import requests
import datetime
import pandas as pd
from PIL import Image
import json
import extra_streamlit_components as stx
from streamlit_option_menu import option_menu

import streamlit_authenticator as stauth

import streamlit.components.v1 as components
# import for sql authentication
import sqlite3 as sql

# Function to get weather info from a suitable weather API using latitude and longitude
def get_hourly_weather_info(latitude, longitude, date_time):
    base_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?"
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    params = {
        "lat": latitude,
        "lon": longitude,
        #"exclude": "current,minutely,daily",  # Exclude unnecessary data
        "appid": "bd5e378503939ddaee76f12ad7a97608",
        "dt": date_time,
        #"units": "metric"  # Units can be metric, imperial, or standard
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            hourly_weather = data.get("current")
            if hourly_weather:
                # Process hourly weather data here as needed
                timestamp = hourly_weather.get("dt")
                weather_info = {
                    "time": datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                    "temperature": hourly_weather.get("temp"),
                    "condition": hourly_weather["weather"][0]["main"],
                    "wind_speed": hourly_weather.get("wind_speed")
                }
                print(weather_info)  # Example: Print weather information
                return weather_info
            else:
                return None
        else:
            return None
    except requests.RequestException as e:
        print("Error fetching data:", e)
        return None

# Fungsi untuk menambahkan catatan memancing
def add_note(username, conn, init_location_details="", init_combined_datetime="", init_fish_type="", init_jumlah_=None, init_bait_used="", init_fishing_method=""):
    st.title("Tambah Catatan Mancing")
    
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
            document.getElementById('lat-span').innerHTML = clickedLat;
            document.getElementById('lon-span').innerHTML = clickedLng;

            // Fungsi untuk mendapatkan nilai latitude dan longitude yang dipilih
            function setCookie(name, value, days) {
                var expires = "";
                if (days) {
                    var date = new Date();
                    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                    expires = "; expires=" + date.toUTCString();
                }
                document.cookie = name + "=" + value + expires + "; path=/";
            }

            // Panggil fungsi ini ketika Anda memiliki nilai latitude dan longitude
            function setCoordinatesInCookie(lat, lon) {
                var coordinates = {'latitude': lat, 'longitude': lon};
                setCookie('coordinates', JSON.stringify(coordinates), 1);
            }
            setCoordinatesInCookie(clickedLat,clickedLng);
        });
    }
        

    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA6JQDWAVYXN07fZAtBK-ATcBg750J68bQ&libraries=places&callback=initMap" async defer></script>
    </body>
    </html>
    """
    
    # Display the HTML content with the map
    components.html(google_maps_autocomplete, height=500)

    if 'clicked_lat' not in st.session_state:
        st.session_state.clicked_lat = None
        st.session_state.clicked_lng = None
    
    # Membaca nilai dari cookie
    @st.cache_resource(experimental_allow_widgets=True)
    def get_manager():
        return stx.CookieManager(key="kukis")

    cookie_manager = get_manager()

    cookies = cookie_manager.get_all()

    def get_cookie_value(cookie_name):
        cookie_value = None
        if "coordinates" in cookies:
            cookie_value = cookie_manager.get(cookie=cookie_name)
        return cookie_value
    checkkoor = False

    if st.button("Simpan Koordinat"):
        # Mendapatkan nilai latitude dan longitude dari cookie
        
        coordinates = get_cookie_value("coordinates")
        st.session_state.clicked_lat = coordinates.get("latitude")
        st.session_state.clicked_lng = coordinates.get("longitude")
        checkkoor = True

    if checkkoor:
        st.write(f'Saved! Latitude: {st.session_state.clicked_lat}, Longitude: {st.session_state.clicked_lng}')
    location_details_ = st.text_input("Detail Lokasi", value=init_location_details)

    
    # Input tanggal
    st.session_state.input_date = st.date_input("Tanggal")

    # Input waktu
    st.session_state.input_time = st.time_input("Waktu")

    # Memasukkan jenis ikan yang ditangkap
    fish_type_ = st.text_input("Jenis Ikan yang Ditangkap", value=init_fish_type)

    jumlah_ = st.number_input("Masukan jumlah ikan", step=1)
    
    # Memasukkan umpan memancing
    bait_used_ = st.selectbox('Jenis Umpan', ['Umpan alami -  Udang','cacing','cacing laut','cumi','pelet','lumut','kodok','potongan ikan','ulat','Umpan buatan - minnow','popper','metal jig','konahead','spoon','crankbait','stckbait','spinner','jig head','soft plastic lure','sabiki (kotrekan)'])

    # Memasukkan metode memancing
    fishing_method_ = st.selectbox('Metode Memancing', ["Bottom Fishing (Mancing Dasaran)", "Fly Lining (Ngoncer)", "Negek Normal", "Negek Ngoyor", "Trolling", "Casting - Poping", "Casting - Surf Fishing", "Casting - Rock Fishing", "Jigging"])

    datetime_ = str(datetime.datetime.combine(st.session_state.input_date, st.session_state.input_time))
    datetime_object = datetime.datetime.strptime(datetime_, "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)

    # Convert the datetime object to epoch time (seconds since the epoch)
    epoch_time = int(datetime_object.timestamp())
    
    weather_infor = get_hourly_weather_info(st.session_state.clicked_lat, st.session_state.clicked_lng, epoch_time)
    
    try:
        if st.session_state.input_time and st.session_state.input_date and st.session_state.clicked_lat:
            weather_infor = get_hourly_weather_info(st.session_state.clicked_lat, st.session_state.clicked_lng, epoch_time)

            weather_text = f"Pada {weather_infor['time']}, suhu udara adalah {weather_infor['temperature'] - 273.15:.2f}°C, " \
                    f"dengan kondisi {weather_infor['condition'].lower()}, " \
                    f"dan kecepatan angin sebesar {weather_infor['wind_speed']} m/s."

            st.text(weather_text)
    except TypeError:
        st.warning("Latitude dan Longitude belum tersimpan, klik Simpan Koordinat kemudian pilih tanggal dan jam kembali")

    if st.button("Simpan Catatan"):
        with conn:
            conn.execute(
                f"INSERT INTO catatan(location_details, datetime, fish_type, fish_get, bait_used, fishing_method, username_catatan) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (location_details_, datetime_, fish_type_, jumlah_, bait_used_, fishing_method_, username)
            )
            st.success("Catatan baru tersimpan")

# Fungsi untuk mengecek catatan
def check_note(username, conn):
    table_data = conn.execute(
        "SELECT location_details, datetime, fish_type, fish_get, bait_used, fishing_method FROM catatan WHERE username_catatan = ?",(username,)).fetchall()   
    if table_data:
        data_to_display = []
        for row in table_data:
            location_details, datetime, fish_type, jumlah_, bait_used, fishing_method = row
            data_to_display.append({
                "Location Details": location_details,
                "Datetime": datetime,
                "Fish Type": fish_type,
                "Total get": jumlah_,
                "Bait Used": bait_used,
                "Fishing Method": fishing_method,
            })
        st.dataframe(data_to_display)  # Use st.dataframe instead of st.data_editor
        
    else:
        st.write("Belum ada catatan")
    
# Fungsi untuk mengedit catatan
def edit_note(username, conn):
    table_data = conn.execute(
        "SELECT id, location_details, datetime, fish_type, fish_get, bait_used, fishing_method FROM catatan WHERE username_catatan = ?",(username,)).fetchall()     
    if table_data:
        selected_id = st.selectbox("Pilih Catatan yang ingin diedit", [f"ID: {row[0]}" for row in table_data])
        
        # Ambil id yang dipilih
        selected_id_row = int(selected_id.split(":")[1].strip())

        data_to_display = []
        for row in table_data:
            if row[0] == selected_id_row:
                data_to_display.append({
                    "Location Details": row[1],
                    "Datetime": row[2],
                    "Fish Type": row[3],
                    "Total get": row[4],
                    "Bait Used": row[5],
                    "Fishing Method": row[6],
                })
                df = pd.DataFrame(data_to_display)
                st.table(df)
            
        if st.checkbox("Edit Catatan"):
            new_location = st.text_input("Masukkan Lokasi Baru")
            if new_location is None:
                new_location = data_to_display[0]["Location Details"]
            new_datetime = st.text_input("Masukkan Waktu Baru")
            if new_datetime is None:
                new_datetime = data_to_display[0]["Datetime"]
            new_fish_type = st.text_input("Masukkan Jenis Ikan Baru")
            if new_fish_type is None:
                new_fish_type = data_to_display[0]["Fish Type"]
            new_total = st.text_input("Masukkan Total baru")
            if new_total is None:
                new_total = data_to_display[0]["Total get"]           
            new_bait_used = st.text_input("Masukkan Umpan Baru")
            if new_bait_used is None:
                new_bait_used = data_to_display[0]["Bait Used"]
            new_fishing_method = st.text_input("Masukkan Metode Memancing Baru")
            if new_fishing_method is None:
                new_fishing_method = data_to_display[0]["Fishing Method"]
            
            if st.button("Simpan Perubahan"):
                conn.execute("UPDATE catatan SET location_details=?, datetime=?, fish_type=?, fish_get=?, bait_used=?, fishing_method=? WHERE id=?",
                             (new_location, new_datetime, new_fish_type, new_total, new_bait_used, new_fishing_method, selected_id))
                st.success(f"Catatan dengan ID {selected_id_row} telah diperbarui.")

    else:
        st.write("Tidak ada catatan untuk diedit")

# Fungsi untuk menghapus catatan
def delete_note(username, conn):
    table_data = conn.execute("SELECT id, location_details, datetime, fish_type, fish_get, bait_used, fishing_method FROM catatan WHERE username_catatan = ?",(username,)).fetchall()    
    
    if table_data:
        selected_id = st.selectbox("Pilih Catatan yang Ingin dihapus", [f"ID: {row[0]}" for row in table_data])
        
        # Ambil id yang dipilih
        selected_id_row = int(selected_id.split(":")[1].strip())

        data_to_display = []
        for row in table_data:
            if row[0] == selected_id_row:
                data_to_display.append({
                    "Location Details": row[1],
                    "Datetime": row[2],
                    "Fish Type": row[3],
                    "Total get": row[4],
                    "Bait Used": row[5],
                    "Fishing Method": row[6],
                })
                df = pd.DataFrame(data_to_display)
                st.table(df)

        if st.button("Hapus Catatan"):
            with conn:
                conn.execute("DELETE FROM catatan WHERE id=?", (selected_id_row,))
            st.success("Catatan telah dihapus")
    else:
        st.write("Tidak ada catatan untuk dihapus")


# Sidebar navigation function
current_page = "Home"  # Inisialisasi status halaman


def button_coiche():
    selected_tab = option_menu(menu_title=None, options=["Lihat Catatan", "Tambah Catatan", "Edit Catatan", "Hapus Catatan"], icons=["journal text", "plus circle", "pencil square", "trash"], key="nav", orientation="horizontal",)
    if selected_tab == "Lihat Catatan":
        check_note(username, conn1)
    elif selected_tab == "Tambah Catatan":
        add_note(username, conn1)
    elif selected_tab == "Edit Catatan":
        edit_note(username, conn1)
    elif selected_tab == "Hapus Catatan":
        delete_note(username, conn1)


st.set_page_config(page_title="Journal Mancing", page_icon="🎣", layout="wide")

st.header("Journal Mancing®")

st.image("https://lh3.googleusercontent.com/u/0/drive-viewer/AK7aPaDNoeXVsyJM3hkZCzFNtF1U4fqnhWuKCbyInbnrygpp15qmOQRE5L9ypbOX3dz_xLctMdcQbZruXlyJkFlf-hB5vDkPSg=w1920-h970")


# ----- SQL AUTH
conn = sql.connect("file:auth.db?mode=ro", uri=True)
conn1 = sql.connect("file:auth.db?mode=rwc", uri=True)
cred_data = conn.execute("select username,password,names from users").fetchall()
conn1.execute("CREATE TABLE IF NOT EXISTS catatan (id INTEGER PRIMARY KEY AUTOINCREMENT, username_catatan VARCHAR(255), location_details TEXT, datetime TIMESTAMP, fish_type VARCHAR(255), fish_get VARCHAR(255), bait_used VARCHAR(255),fishing_method VARCHAR(255))")

names = []
usernames = []
passwords = []
credentials = {"usernames":{}}

if cred_data:
    cred_data2 = list(zip(*cred_data))
    usernames = cred_data2[0]
    passwords = cred_data2[1]
    names = cred_data2[2]
    hasher = stauth.Hasher()
    hashed_passwords = []
    for password in passwords:
        hashed_passwords.append(hasher.hash(password))
    for un, pw, name in zip(usernames,hashed_passwords,names):
        user_dict = {"name":name,"password":pw}
        credentials["usernames"].update({un:user_dict})
else:
    st.write("No entries in authentication database")

authenticator = stauth.Authenticate(credentials, "data_mancing", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", location="main")
st.session_state.username = username
st.session_state.name = name

if authentication_status == False:
    st.error("Username/password salah")
if authentication_status == None:
    st.warning("Masukan Username dan Password")

if authentication_status:
    def main_page():
        st.title("Home Page")
        button_coiche()

    def main():
        authenticator.logout("Logout","sidebar")
        st.sidebar.title(f"Welcome {name}")
        main_page()
            
    if __name__ == "__main__":
        main()
