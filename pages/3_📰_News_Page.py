import streamlit as st
import requests
import datetime
import pandas as pd
from PIL import Image
import json
import extra_streamlit_components as stx

import streamlit_authenticator as stauth

import streamlit.components.v1 as components
# import for sql authentication
import sqlite3 as sql

# Define a function to display news or information
def display_news():
    st.title("Informasi dan Berita")

    news_conn = sql.connect("file:news.db?mode=ro", uri=True)
    news = news_conn.execute("select title, content, image_url, date_published from news ORDER BY date_published DESC").fetchall()

    if news:
        for row in news:
            title, content, image_url, date_published = row
            st.header(title)
            st.caption(date_published)
            st.image(image_url)
            st.write(content)
    else:
        st.write("Belum ada catatan")





# Use the function to display the news/information page
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
    hashed_passwords = hasher.hash(list(passwords))  # Convert tuple to list
    for un, pw, name in zip(usernames,hashed_passwords,names):
        user_dict = {"name":name,"password":pw}
        credentials["usernames"].update({un:user_dict})
else:
    st.write("No entries in authentication database")

authenticator = stauth.Authenticate(credentials, "data_mancing", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    def main_page():
        display_news()

    def main():
        authenticator.logout("Logout","sidebar")
        st.sidebar.title(f"Welcome {name}")
        main_page()
            
    if __name__ == "__main__":
        main()
