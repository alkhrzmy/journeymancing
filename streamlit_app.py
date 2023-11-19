import streamlit as st
import mysql.connector

# Koneksi ke database
def create_connection():
    conn = mysql.connector.connect(
        host='hostname',
        user='username',
        password='password',
        database='nama_database'
    )
    return conn

# Fungsi untuk mengambil data pengguna dari database
def get_user(username):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Fungsi untuk verifikasi password
def verify_password(stored_password, provided_password):
    # Di sini, bisa digunakan fungsi hashing untuk membandingkan password yang terenkripsi.
    # Misalnya, bcrypt atau SHA256, tetapi untuk contoh sederhana, kita akan langsung membandingkan.
    return stored_password == provided_password

def main():
    st.title('Journey Mancing')
    st.image('background_image.jpg', use_column_width=True)

    # Tampilkan form login
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        user = get_user(username)
        if user:
            if verify_password(user['password'], password):
                st.success('Login berhasil!')
                # Lanjutkan ke halaman selanjutnya setelah login berhasil
                # Di sini kamu bisa menambahkan kode untuk menavigasi ke halaman berikutnya
            else:
                st.error('Password salah. Silakan coba lagi.')
        else:
            st.error('Username tidak ditemukan.')

if __name__ == '__main__':
    main()
