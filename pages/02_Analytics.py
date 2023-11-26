import streamlit as st
import extra_streamlit_components as stx
import streamlit.components.v1 as components

st.header("Analytics Journal Mancing")
from datetime import datetime, timezone

# Input tanggal
input_date = st.date_input("Tanggal")

# Input waktu
input_time = st.time_input("Waktu")

fishing_method_ = st.selectbox('Metode Memancing', ["Bottom Fishing (Mancing Dasaran)", "Fly Lining (Ngoncer)", "Negek Normal", "Negek Ngoyor", "Trolling", "Casting - Poping", "Casting - Surf Fishing", "Casting - Rock Fishing", "Jigging"])

# Memasukkan umpan memancing
bait_used_ = st.selectbox('Jenis Umpan', ['Umpan alami -  Udang','cacing','cacing laut','cumi','pelet','lumut','kodok','potongan ikan','ulat','Umpan buatan - minnow','popper','metal jig','konahead','spoon','crankbait','stckbait','spinner','jig head','soft plastic lure','sabiki (kotrekan)'])


st.write(fishing_method_)
# Menggabungkan tanggal dan waktu menjadi objek datetime
datetime_ = str(datetime.combine(input_date, input_time))

datetime_object = datetime.strptime(datetime_, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

# Convert the datetime object to epoch time (seconds since the epoch)
epoch_time = int(datetime_object.timestamp())
st.write(epoch_time)

weather_embed = """
<!DOCTYPE html>
<html>

<head>
  <title>Weather App</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
  <link href="http://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
  <style type="text/css">
    body{
        margin: 0;
        padding: 0;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Poppins', sans-seriff;
        color: #fff;
        background:  transparent;
    }
    .container {
        width: 26%;
    }
    .card {
        border-radius: 50px;
        background: #343434;
        box-shadow: 5px 5px 10px #191b1b, -5px -5px 10px #595959;
        padding: 3%;
        text-align: center;
    }
    .card h4 {
        font-size: 4rem;
        font-weight: 400;
        margin: 1rem 0;
    }
    img#icon {
        width: 20%;
    }
    h6#weather{
        text-transform: capitalize;
    }
    button.refresh {
        display: block;
        width: 100px;
        margin: 10px auto;
        border: 0;
        background: transparent;
        color: #9c9c9d;
        font-size: 30px;
        height: 100px;
        border-radius: 50%;
        box-shadow: 10px 4px 18px #252525, 5px 5px 18px #4a4a4a;
        transition: 0.3s;
    }
    button.refresh:hover{
        box-shadow: inset 10px 4px 18px #252525, inset 5px 5px 18px #4a4a4a;
    }
    </style>
</head>

<body>
  <div class="container">
    <div class="card">
      <h2><i class="fa fa-map-marker"></i> <span id="location"></span></h2>
      <h6 id="weather"></h6>
      <h4><span id="temp"></span><sup>o</sup>C</h4>
      <img id="icon" src="">
      <button onClick="window.location.reload();" class="refresh"><i class="fa fa-refresh"></i></button>
    </div>
  </div>
</body>
<script src="https://code.jquery.com/jquery-3.4.1.min.js"
  integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
<script type="text/javascript">
  link = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=" + ;
  var request = new XMLHttpRequest();
  request.open('GET', link, true);
  request.onload = function () {
    var obj = JSON.parse(this.response);
    console.log(obj);

    document.getElementById('weather').innerHTML = obj.weather[0].description;
    document.getElementById('location').innerHTML = obj.name;
    document.getElementById('temp').innerHTML = obj.main.temp - 273.15;
    document.getElementById('icon').src = "http://openweathermap.org/img/w/" + obj.weather[0].icon + ".png";

    if (request.status >= 200 && request.status < 400) {
      var temp = obj.main.temp;
    }
    else {
      console.log("The city doesn't exist! Kindly check");
    }
  }
  request.send();
</script>

</html>
"""
components.html(weather_embed, width=400, height=400)