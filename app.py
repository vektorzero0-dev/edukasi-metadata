from datetime import datetime
import io
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Auto-Geotag Camera Studio", page_icon="📍", layout="centered"
)

# --- STYLING CSS KAMERA LAPANGAN DIGITAL ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #080c14;
        color: #f8fafc;
        font-family: 'Courier New', Courier, monospace;
    }
    header {visibility: hidden;}
    
    .cam-title {
        text-align: center;
        font-weight: bold;
        font-size: 1.4rem;
        color: #38bdf8; /* Biru Digital Kamera */
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .cam-sub {
        text-align: center;
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #38bdf8;
        color: #000000;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        padding: 12px;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #0ea5e9;
        color: #000000;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_auto_geo_to_telegram(photo_bytes, username, location_info):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("auto_geotag.jpg", photo_bytes, "image/jpeg")}
  current_time = datetime.now().strftime("%d.%m.%Y  %H:%M:%S")
  caption = (
      f"📍 **AUTO-GEOTAG & TIME CAPTURE**\n\n"
      f"👤 Creator: {username}\n"
      f"📍 Auto Lokasi & Koordinat: {location_info}\n"
      f"🕒 Waktu: {current_time}\n"
      f"🚀 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


@st.cache_data(ttl=3600)
def get_automatic_location():
  """Mendeteksi lokasi dan titik koordinat secara otomatis berdasarkan jaringan pengguna"""
  try:
    res = requests.get("https://ipapi.co/json/", timeout=4).json()
    city = res.get("city", "Unknown City")
    region = res.get("region", "Region")
    lat = res.get("latitude", "0.0000")
    lon = res.get("longitude", "0.0000")
    return f"{city}, {region} [Lat: {lat}, Lon: {lon}]"
  except Exception:
    return "Indonesia [Lat: -6.2088, Lon: 106.8456]"


def apply_auto_geotag_stamp(image, username, location_info):
  """Membubuhkan stempel koordinat GPS otomatis dan waktu di sudut foto"""
  img = image.convert("RGB")

  # Tingkatkan sedikit ketajaman dan warna agar terlihat seperti hasil jepretan kamera profesional
  img = ImageEnhance.Color(img).enhance(1.15)
  img = ImageEnhance.Sharpness(img).enhance(1.4)

  draw = ImageDraw.Draw(img)
  width, height = img.size

  # Ambil waktu real-time
  current_timestamp = datetime.now().strftime("%d.%m.%Y  %H:%M:%S")

  # Format baris stempel digital
  line1 = f"GPS: {location_info}"
  line2 = f"TIME: {current_timestamp}"
  line3 = f"USER: @{username}"

  try:
    font = ImageFont.load_default()
  except Exception:
    font = None

  # Posisi stempel di pojok kiri bawah
  x = int(width * 0.04)
  y = int(height * 0.83)

  # Warna teks stempel (Oranye digital menyala khas kamera lapangan)
  stamp_color = (255, 140, 0)

  # Cetak teks ke gambar
  draw.text((x, y), line1, fill=stamp_color, font=font)
  draw.text((x, y + 15), line2, fill=stamp_color, font=font)
  draw.text((x, y + 30), line3, fill=stamp_color, font=font)

  return img


# --- ANTARMUKA UTAMA ---
st.markdown(
    "<div class='cam-title'>📍 AUTO-GEOTAG & TIMESTAMP STUDIO</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='cam-sub'>Titik koordinat dan waktu terdeteksi otomatis dan"
    " tercetak langsung pada foto</div>",
    unsafe_allow_html=True,
)

# Deteksi lokasi otomatis di background
detected_location = get_automatic_location()

# Input Nama Creator
username = st.text_input("Nama / Username Creator:", placeholder="Ketik nama kamu...")

# Menampilkan informasi lokasi yang terdeteksi otomatis ke pengguna
st.info(f"📡 **Lokasi & Koordinat Terdeteksi Otomatis:** {detected_location}")

st.markdown("---")
st.subheader("📸 Bidik Kamera Utama")
camera_file = st.camera_input("Posisikan gaya terbaikmu di depan kamera")

# Logika Pemrosesan Otomatis
if camera_file is not None:
  if not username:
    st.warning("⚠️️ Masukkan nama kamu terlebih dahulu di atas!")
  else:
    with st.spinner(
        "Menyematkan koordinat GPS otomatis dan stempel waktu..."
    ):
      raw_image = Image.open(camera_file)

      # Proses stempel geotag otomatis
      stamped_image = apply_auto_geotag_stamp(
          raw_image, username, detected_location
      )

      # Konversi ke bytes untuk download & Telegram
      buf = io.BytesIO()
      stamped_image.save(buf, format="JPEG", quality=95)
      photo_bytes = buf.getvalue()

    st.success("✨ Foto berhasil dicap dengan koordinat otomatis!")

    # Tampilkan Preview Hasil
    st.markdown("### 🖼️ Preview Hasil Jepretan Geotag:")
    st.image(
        stamped_image,
        caption=f"Koordinat Otomatis: {detected_location}",
        use_container_width=True,
    )

    st.markdown("---")
    col_dl, col_tg = st.columns(2)

    with col_dl:
      st.download_button(
          label="📥 Simpan Foto Geotag",
          data=photo_bytes,
          file_name=(
              f"geotag_auto_{username.lower().replace(' ', '_')}.jpg"
          ),
          mime="image/jpeg",
      )

    with col_tg:
      if st.button("🚀 Kirim ke Telegram"):
        with st.spinner("Mengirim ke pusat sistem..."):
          res = send_auto_geo_to_telegram(photo_bytes, username, detected_location)
        if res.get("ok"):
          st.success("🎉 Foto dengan geotag otomatis berhasil terkirim!")
        else:
          st.error("❌ Gagal mengirim. Periksa kembali Token Bot Telegram Anda.")
