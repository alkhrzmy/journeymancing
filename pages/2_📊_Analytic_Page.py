import streamlit as st
import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import plotly.express as px

st.title(f"Insight Mancing {st.session_state.name}")

# Visualisasi Metode Mancing
st.subheader("Summary Metode Mancing Yang Sering Digunakan")

conn = sql.connect("file:auth.db?mode=rwc", uri=True)
table_method = conn.execute(
"SELECT fishing_method FROM catatan WHERE username_catatan = ?",(st.session_state.username,)).fetchall()
df_method = pd.DataFrame(table_method, columns=[0])

# Membuat visualisasi diagram batang
if 'df_method' in locals() and not df_method.empty and 0 in df_method.columns:
    st.bar_chart(df_method[0].value_counts())
else:
    st.write("No fishing method data available for visualization")


# Visualisasi Metode per Ikan
# Similarly for the fish per method visualization:
if 'df_fishpermethod' in locals() and not df_fishpermethod.empty:
    # Check for empty values in columns
    if df_fishpermethod['Metode'].empty or df_fishpermethod['Jumlah'].empty:
        st.write("Insufficient data for visualization")
    else:
        st.title("Visualisasi Data Metode per Ikan")
        table_fishpermethod = conn.execute(
        "SELECT fishing_method,fish_get FROM catatan WHERE username_catatan = ?",(st.session_state.username,)).fetchall()
        df_fishpermethod = pd.DataFrame(table_fishpermethod, columns=["Metode", "Jumlah"])
        df_fishpermethod["Jumlah"] = pd.to_numeric(df_fishpermethod["Jumlah"])

        # Membuat visualisasi diagram batang grup
        st.bar_chart(df_fishpermethod.groupby("Metode")["Jumlah"].sum())


# Visualisasi Umpan per Ikan
# Similarly for the fish per method visualization:
if 'df_fishpermethod' in locals() and not df_fishpermethod.empty:
    # Check for empty values in columns
    if df_fishpermethod['Metode'].empty or df_fishpermethod['Jumlah'].empty:
        st.write("Insufficient data for visualization")
    else:
        st.title("Visualisasi Data Umpan per Ikan")
        table_fishpermethod = conn.execute(
        "SELECT bait_used,fish_get FROM catatan WHERE username_catatan = ?",(st.session_state.username,)).fetchall()
        df_fishpermethod = pd.DataFrame(table_fishpermethod, columns=["Umpan", "Jumlah"])
        df_fishpermethod["Jumlah"] = pd.to_numeric(df_fishpermethod["Jumlah"])

# Membuat visualisasi diagram batang grup
# Similarly for the fish per method visualization:
if 'df_fishpermethod' in locals() and not df_fishpermethod.empty:
    # Check for empty values in columns
    if df_fishpermethod['Metode'].empty or df_fishpermethod['Jumlah'].empty:
        st.write("Insufficient data for visualization")
    else:
        st.bar_chart(df_fishpermethod.groupby("Umpan")["Jumlah"].sum())


st.title("Visualisasi Data per Bulan")
# Visualisasi Ikan per Bulan Tahun
table_fishperdate = conn.execute(
"SELECT datetime,fish_get FROM catatan WHERE username_catatan = ?",(st.session_state.username,)).fetchall()
df_fishperdate = pd.DataFrame(table_fishperdate, columns=["Timestamp", "Jumlah"])

# 
df_fishperdate = df_fishperdate.sort_values(by="Timestamp")

# Mengonversi kolom "Timestamp" menjadi tipe data datetime
df_fishperdate["Timestamp"] = pd.to_datetime(df_fishperdate["Timestamp"])

# Membuat visualisasi diagram batang dengan st.bar_chart
fig = px.line(df_fishperdate, x="Timestamp", y="Jumlah", title="Visualisasi Data per Bulan", labels={"Jumlah": "Jumlah Ikan"})
st.plotly_chart(fig)
