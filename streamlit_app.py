import streamlit as st
import sqlite3
from datetime import datetime

# Fungsi untuk membuat tabel catatan memancing jika belum ada
def create_table():
    conn = sqlite3.connect('fishing_notes.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS fishing_notes (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  tanggal DATE,
                  lokasi TEXT,
                  hasil TEXT
              )
              ''')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan catatan memancing ke database
def add_fishing_note(tanggal, lokasi, hasil):
    conn = sqlite3.connect('fishing_notes.db')
    c = conn.cursor()
    c.execute('INSERT INTO fishing_notes (tanggal, lokasi, hasil) VALUES (?, ?, ?)', (tanggal, lokasi, hasil))
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

# Membuat tabel jika belum ada
create_table()

# Judul halaman
st.title('Catatan Memancing')

# Formulir untuk menambahkan catatan memancing
st.header('Tambah Catatan Memancing')
tanggal = st.date_input('Tanggal')
lokasi = st.text_input('Lokasi')
hasil = st.text_area('Hasil Memancing')
if st.button('Tambah Catatan'):
    add_fishing_note(tanggal, lokasi, hasil)
    st.success('Catatan berhasil ditambahkan!')

# Menampilkan catatan memancing
st.header('Catatan Memancing')
catatan_memancing = show_fishing_notes()
if catatan_memancing:
    for catatan in catatan_memancing:
        st.write(f"**Tanggal:** {catatan[1]}, **Lokasi:** {catatan[2]}, **Hasil:** {catatan[3]}")
else:
    st.warning('Belum ada catatan memancing.')

