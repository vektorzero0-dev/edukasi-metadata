from datetime import datetime
import io
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Timestamp & Geotag Camera", page_icon="📍", layout="centered"
)

# --- STYLING CSS KAMERA LAPANGAN / DIGITAL JADUL ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
        font-family: 'Courier New', Courier, monospace;
    }
    header {visibility: hidden;}
    
    .stamp-header {
        text-align: center;
        font-weight: bold;
        font-size: 1.3rem;
        color: #f59e0b; /* Warna Oranye Khas Stempel Kamera Jadul */
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .stamp-sub {
        text-align: center;
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #f59e0b;
        color: #000000;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        padding: 10px;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #d97706;
        color: #000000;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_geo_photo_to_telegram(photo_bytes, username, location):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("geotag_selfie.jpg", photo_bytes, "image/jpeg")}
  current_time = datetime.now().strftime("%d.%m.%Y  %H:%M:%S")
  caption = (
      f"📍 **TIMESTAMP & GEOTAG CAPTURE**\n\n"
      f"👤 Creator: {username}\n"
      f"📍 Lokasi: {location}\n"
      f"🕒 Waktu: {current_time}\n"
      f"🚀 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def apply_timestamp_and_geotag(image, username, location_text):
  """Menambahkan stempel waktu digital dan geotag persis di sudut foto"""
  img = image.convert("RGB")

  # Sedikit tingkatkan kejernihan dan warna natural
  img = ImageEnhance.Color(img).enhance(1.1)
  img = ImageEnhance.Sharpness(img).enhance(1.3)

  draw = ImageDraw.Draw(img)
  width, height = img.size

  # Ambil waktu lokal saat ini
  current_timestamp = datetime.now().strftime("%d.%m.%Y  %H:%M:%S")

  # Teks yang akan dicetak di foto
  line1 = f"LOC: {location_text.upper()}"
  line2 = f"TIME: {current_timestamp}"
  line3 = f"USER: @{username}"

  # Menggunakan font bawaan PIL (aman di semua server tanpa file font tambahan)
  try:
    font = ImageFont.load_default()
  except Exception:
    font = None

  # Koordinat awal stempel di pojok kiri bawah foto
  x = int(width * 0.05)
  y = int(height * 0.85)

  # Gambar kotak latar belakang semi-transparan tipis untuk stempel agar mudah dibaca
  # (Opsional: menggambar teks langsung dengan warna oranye digital khas kamera)
  text_color = (255, 140, 0)  # Oranye digital terang

  # Gambar teks ke gambar
  draw.text((x, y), line1, fill=text_color, font=font)
  draw.text((x, y + 15), line2, fill=text_color, font=font)
  draw.text((x, y + 30), line3, fill=text_color, font=font)

  return img


# --- ANTARMUKA UTAMA ---
st.markdown(
    "<div class='stamp-header'>📍 TIMESTAMP & GEOTAG CAMERA</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='stamp-sub'>Setiap foto yang dijepret otomatis dilengkapi stempel"
    " waktu dan lokasi akurat</div>",
    unsafe_allow_html=True,
)

# 1. Input Identitas & Lokasi (Geotag)
username = st.text_input("Nama / Username Creator:", placeholder="Ketik nama kamu...")
location_input = st.text_input(
    "Lokasi / Geotag (Contoh: Jakarta Pusat / Studio 01):",
    placeholder="Ketik lokasi saat ini...",
)

st.markdown("---")
st.subheader("📸 Bidik Kamera Utama")
camera_file = st.camera_input("Posisikan gaya terbaikmu")

# 2. Logika Proses Penempelan Stempel
if camera_file is not None:
  if not username or not location_input:
    st.warning("⚠️ Harap isi Nama dan Lokasi terlebih dahulu di atas!")
  else:
    with st.spinner("Menambahkan stempel waktu dan geotag ke foto..."):
      raw_image = Image.open(camera_file)

      # Proses stempel waktu & lokasi
      stamped_image = apply_timestamp_and_geotag(
          raw_image, username, location_input
      )

      # Konversi ke bytes untuk diunduh & dikirim
      buf = io.BytesIO()
      stamped_image.save(buf, format="JPEG", quality=95)
      photo_bytes = buf.getvalue()

    st.success("✨ Foto berhasil diberi stempel waktu dan lokasi!")

    # Tampilkan Preview
    st.markdown("### 🖼️ Preview Hasil Stempel:")
    st.image(
        stamped_image,
        caption=f"Lokasi: {location_input} | Waktu: Real-time",
        use_container_width=True,
    )

    st.markdown("---")
    col_dl, col_tg = st.columns(2)

    with col_dl:
      st.download_button(
          label="📥 Simpan Foto Stempel",
          data=photo_bytes,
          file_name=(
              f"geotag_shot_{username.lower().replace(' ', '_')}.jpg"
          ),
          mime="image/jpeg",
      )

    with col_tg:
      if st.button("🚀 Kirim ke Telegram"):
        with st.spinner("Mengirim ke pusat sistem..."):
          res = send_geo_photo_to_telegram(photo_bytes, username, location_input)
        if res.get("ok"):
          st.success("🎉 Foto berstempel berhasil terkirim ke Telegram!")
        else:
          st.error("❌ Gagal mengirim. Periksa kembali Token Bot Telegram Anda.")
