import streamlit as st
import pandas as pd

# Membuat DataFrame untuk menyimpan catatan memancing
catatan_memancing = pd.DataFrame(columns=['Tanggal', 'Lokasi', 'Jenis Ikan', 'Cuaca', 'Peralatan', 'Catatan'])

# Fungsi untuk menambahkan catatan memancing
def tambah_catatan(tanggal, lokasi, jenis_ikan, cuaca, peralatan, catatan):
    global catatan_memancing
    catatan_memancing = catatan_memancing.append({
        'Tanggal': tanggal,
        'Lokasi': lokasi,
        'Jenis Ikan': jenis_ikan,
        'Cuaca': cuaca,
        'Peralatan': peralatan,
        'Catatan': catatan
    }, ignore_index=True)

# Halaman utama
def main():
    st.title("Catatan Memancing")

    # Sidebar untuk menambahkan catatan
    st.sidebar.header("Tambah Catatan")
    tanggal = st.sidebar.date_input("Tanggal", pd.to_datetime('today'))
    lokasi = st.sidebar.text_input("Lokasi")
    jenis_ikan = st.sidebar.text_input("Jenis Ikan")
    cuaca = st.sidebar.text_input("Cuaca")
    peralatan = st.sidebar.text_input("Peralatan")
    catatan = st.sidebar.text_area("Catatan")
    
    if st.sidebar.button("Simpan Catatan"):
        tambah_catatan(tanggal, lokasi, jenis_ikan, cuaca, peralatan, catatan)

    # Menampilkan catatan yang telah disimpan
    st.subheader("Catatan Memancing yang Telah Disimpan")
    st.dataframe(catatan_memancing)

if __name__ == "__main__":
    main()
