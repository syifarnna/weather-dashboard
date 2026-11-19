"""Dashboard Cuaca Indonesia — Streamlit + Open-Meteo API."""
import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Dashboard Cuaca", page_icon="🌤️", layout="wide")

KOTA = {
    "Jakarta": (-6.2, 106.8),
    "Bandung": (-6.9, 107.6),
    "Surabaya": (-7.25, 112.75),
    "Yogyakarta": (-7.8, 110.4),
    "Medan": (3.6, 98.67),
    "Makassar": (-5.15, 119.43),
    "Denpasar": (-8.65, 115.22),
}

st.title("🌤️ Dashboard Cuaca Indonesia")
st.caption("Data 7 hari ke depan dari Open-Meteo (gratis, tanpa API key)")

pilihan = st.multiselect(
    "Pilih kota:",
    list(KOTA),
    default=["Jakarta", "Bandung", "Surabaya"],
)

@st.cache_data(ttl=1800)
def ambil_cuaca(nama, lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        "&timezone=Asia%2FJakarta&forecast_days=7"
    )
    d = requests.get(url, timeout=15).json()["daily"]
    df = pd.DataFrame({
        "Tanggal": pd.to_datetime(d["time"]),
        "T Max (°C)": d["temperature_2m_max"],
        "T Min (°C)": d["temperature_2m_min"],
        "Hujan (%)": d["precipitation_probability_max"],
    })
    df.insert(0, "Kota", nama)
    return df

if pilihan:
    data = pd.concat([ambil_cuaca(k, *KOTA[k]) for k in pilihan])
    today = pd.Timestamp.today().normalize()
    dates = data["Tanggal"].unique()
    chosen = today if today in dates else pd.Timestamp(dates[0])
    latest = data[data["Tanggal"] == chosen]
    st.subheader(f"Ringkasan ({chosen:%A, %d %b %Y})")
    cols = st.columns(len(pilihan))
    for col, (_, row) in zip(cols, latest.iterrows()):
        emoji = "🌧️" if row["Hujan (%)"] >= 60 else "⛅" if row["Hujan (%)"] >= 30 else "☀️"
        col.metric(f"{emoji} {row['Kota']}",
                   f"{row['T Max (°C)']:.0f}°C",
                   f"min {row['T Min (°C)']:.0f}°C")

    # --- Grafik suhu 7 hari ---
    st.subheader("Suhu 7 hari ke depan")
    fig = go.Figure()
    for k in pilihan:
        df = data[data["Kota"] == k]
        fig.add_trace(go.Scatter(x=df["Tanggal"], y=df["T Max (°C)"],
                                 name=f"{k} (max)", mode="lines+markers"))
        fig.add_trace(go.Scatter(x=df["Tanggal"], y=df["T Min (°C)"],
                                 name=f"{k} (min)", mode="lines", line=dict(dash="dot")))
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=20, b=10),
                      yaxis_title="°C", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # --- Peluang hujan ---
    st.subheader("Peluang hujan maksimal (%)")
    fig2 = go.Figure()
    for k in pilihan:
        df = data[data["Kota"] == k]
        fig2.add_trace(go.Bar(x=df["Tanggal"], y=df["Hujan (%)"], name=k))
    fig2.update_layout(barmode="group", height=350,
                       margin=dict(l=10, r=10, t=20, b=10), yaxis_range=[0, 100])
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("Lihat data mentah"):
        st.dataframe(data, use_container_width=True)
else:
    st.info("Pilih minimal satu kota di atas 👆")
