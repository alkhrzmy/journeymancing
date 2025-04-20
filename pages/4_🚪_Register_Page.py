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

def auth(sidebar=True):

    try:
        conn = sql.connect("file:auth.db?mode=ro", uri=True)
    except sql.OperationalError:
        st.error(
            "Authentication Database is Not Found.\n\nConsider running authlib script in standalone mode to generate."
        )
        return None

    input_widget = st.sidebar.text_input if sidebar else st.text_input
    checkbox_widget = st.sidebar.checkbox if sidebar else st.checkbox
    user = input_widget("Username:")

    data = conn.execute("select * from users where username = ?", (user,)).fetchone()
    if user:
        password = input_widget("Enter Password:", type="password")
        if data and password == data[2]:
            if data[3]:
                if checkbox_widget("Check to edit user database"):
                    _superuser_mode()
            return user
        else:
            return None
    return None

def access_news():
    mode = st.radio("Select", ("Write News", "Delete News"))
    
    if mode == "Write News":
        write_news()
    elif mode == "Delete News":
        delete_news()

def write_news():
    news_conn = sql.connect("file:news.db?mode=rwc", uri=True)
    new_title = st.text_input("Masukan Judul")
    new_content = st.text_area("Masukan isi content")
    new_image_url = st.text_input("Masukan link foto")
    new_date_published = datetime.datetime.now()
    

    if st.button("Buat Berita"):
            with news_conn:
                news_conn.execute(
                    "INSERT INTO news(title, content, image_url, date_published) VALUES (?, ?, ?, ?)",
                    (new_title, new_content, new_image_url, new_date_published)
                )
                st.success("Berita baru tersimpan")

def delete_news():
    news_conn = sql.connect("file:news.db?mode=rwc", uri=True)
    news_list = [x[0] for x in news_conn.execute("select * from news").fetchall()]
    news_list.insert(0, "")
    news_ = st.selectbox("Pilih news", options=news_list)
    if news_:
        if st.button(f"Hapus {news_}"):
            with news_conn:
                news_conn.execute("delete from news where title = ?", (news_,))
                st.write(f"Berita {news_} deleted")



def _list_users(conn):
    table_data = conn.execute("select username,password,names from users").fetchall()
    if table_data:
        table_data2 = list(zip(*table_data))
        st.table(
            {
                "Username": (table_data2)[0],
                "Password": table_data2[1],
                "Name": table_data2[2],
            }
        )
    else:
        st.write("No entries in authentication database")


def _create_users(conn, init_user="", init_pass="", init_super=""):
    user = st.text_input("Enter Username", value=init_user)
    pass_ = st.text_input("Enter Password (required)", value=init_pass)
    super_ = st.text_input("Enter Name", value=init_super)
    if st.button("Update Database") and user and pass_:
        with conn:
            conn.execute(
                "INSERT INTO USERS(username, password, names) VALUES(?,?,?)",
                (user, pass_, super_),
            )
            st.text("Database Updated")


def _edit_users(conn):
    userlist = [x[0] for x in conn.execute("select username from users").fetchall()]
    userlist.insert(0, "")
    edit_user = st.selectbox("Select user", options=userlist)
    if edit_user:
        user_data = conn.execute(
            "select username,password,names from users where username = ?", (edit_user,)
        ).fetchone()
        _create_users(
            conn=conn,
            init_user=user_data[0],
            init_pass=user_data[1],
            init_super=user_data[2],
        )


def _delete_users(conn):
    userlist = [x[0] for x in conn.execute("select username from users").fetchall()]
    userlist.insert(0, "")
    del_user = st.selectbox("Select user", options=userlist)
    if del_user:
        if st.button(f"Press to remove {del_user}"):
            with conn:
                conn.execute("delete from users where username = ?", (del_user,))
                st.write(f"User {del_user} deleted")


def access_db():
    mode = st.radio("Select mode", ("View", "Create", "Edit", "Delete"))
    {
        "View": _list_users,
        "Create": _create_users,
        "Edit": _edit_users,
        "Delete": _delete_users,
    }[mode](
        conn
    )  # I'm not sure whether to be proud or horrified about this...
    

def _superuser_mode():
    st.title("Administator")
    with sql.connect("file:auth.db?mode=rwc", uri=True) as conn:
        conn.execute(
            "create table if not exists users (id INTEGER PRIMARY KEY, username UNIQUE ON CONFLICT REPLACE, password, names)"
        )
    database, news = st.tabs(["Akses Database", "Buat Berita"])
    with database:
        access_db()
    with news:
        access_news()

if __name__ == "__main__":
    st.write(
        "Warning, Admin mode\n\nUse this mode to initialise authentication database"
    )
    if st.checkbox("Login as Admin"):
        
        conn = sql.connect("file:admin.db?mode=rwc", uri=True)
        cred_data = conn.execute("select admin_username, admin_password, names from admin_users").fetchall()

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

        authenticator.login("Login", "main", location="main")  # title, key, location

        if authentication_status == False:
            st.error("Username/password salah")
        if authentication_status == None:
            st.warning("Masukan Username dan Password")

        table_data = conn.execute("select admin_username from admin_users").fetchall()
        if table_data:
            data_to_display = [row[0] for row in table_data]  # Extracting usernames from fetched data

            if username in data_to_display:  
                if authentication_status:
                    _superuser_mode()
                    authenticator.logout("Logout", "sidebar")
            else:
                st.warning("Anda tidak login dengan akun admin")
                st.warning("Logout terlebih dahulu")
                authenticator.logout("Logout")

                
    else:
        if st.checkbox("Registrasi"):
            st.title("Registrasi akun baru")
            user = st.text_input("Enter Username")
            pass_ = st.text_input("Enter Password (required)")
            super_ = st.text_input("Enter Name")
            conn = sql.connect("file:auth.db?mode=rwc", uri=True)
            if st.button("Buat akun") and user and pass_:
                with conn:
                    conn.execute(
                        "INSERT INTO USERS(username, password, names) VALUES(?,?,?)",
                        (user, pass_, super_),
                    )
                    st.success("Akun baru dibuat")

