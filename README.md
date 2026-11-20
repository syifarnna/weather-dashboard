# 🌤️ Dashboard Cuaca Indonesia

Dashboard interaktif cuaca 7 hari ke depan untuk kota-kota besar Indonesia.

Dibuat dengan **Streamlit + Plotly**, data dari **Open-Meteo API** (gratis, tanpa API key).

## Fitur
- 📊 Ringkasan suhu max/min hari ini per kota
- 📈 Grafik suhu 7 hari ke depan (interaktif)
- 🌧️ Peluang hujan maksimal per kota
- 🏙️ Pilih beberapa kota sekaligus

## Menjalankan lokal
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Live demo
🌐 **https://syifarnna.github.io/weather-dashboard/** (GitHub Pages, HTML murni)

Versi Streamlit: jalankan lokal dengan perintah di atas.
