import io
import cv2
import numpy as np
from PIL import Image
import requests
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Real ToonMe AI Studio", page_icon="🎨", layout="centered"
)

# --- STYLING CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    header {visibility: hidden;}
    .studio-title {
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 800;
        font-size: 1.8rem;
        color: #ff5722;
        margin-bottom: 0px;
    }
    .studio-sub {
        text-align: center;
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_cartoon_to_telegram(photo_bytes, username):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("real_toon.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"🎨 **REAL TOONME CAPTURE**\n\n"
      f"👤 User: {username}\n"
      f"✨ Efek: Clean OpenCV Cartoon\n"
      f"🚀 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def convert_to_real_cartoon(pil_image):
  """Mengubah foto menjadi kartun mulus menggunakan OpenCV (cv2)"""
  # Konversi PIL Image ke Numpy Array BGR
  img_np = np.array(pil_image.convert("RGB"))
  img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

  # 1. Buat Masker Garis Tepi (Edges) yang bersih
  gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
  gray_blur = cv2.medianBlur(gray, 7)
  edges = cv2.adaptiveThreshold(
      gray_blur,
      255,
      cv2.ADAPTIVE_THRESH_MEAN_C,
      cv2.THRESH_BINARY,
      blockSize=9,
      C=2,
  )

  # 2. Haluskan warna kulit wajah menggunakan Bilateral Filter berulang
  color = img_bgr
  for _ in range(4):
    color = cv2.bilateralFilter(color, d=9, sigmaColor=75, sigmaSpace=75)

  # 3. Gabungkan warna halus dengan garis tepi kartun
  cartoon = cv2.bitwise_and(color, color, mask=edges)

  # Kembalikan ke format PIL Image RGB
  cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
  return Image.fromarray(cartoon_rgb)


# --- ANTARMUKA APLIKASI ---
st.markdown("<div class='studio-title'>🎨 ToonMe Pro Studio</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='studio-sub'>Ubah foto wajahmu jadi kartun bersih dan estetik"
    " secara instan!</div>",
    unsafe_allow_html=True,
)

# 1. Input Nama Pengguna
username = st.text_input("Masukkan Nama Kamu:", placeholder="Ketik nama di sini...")

st.markdown("---")
st.subheader("📸 Ambil Foto Kamera Depan")
camera_file = st.camera_input("Posisikan wajahmu dengan pas dan tunjukkan senyumanmu")

# 2. Logika Proses Otomatis
if camera_file is not None:
  if not username:
    st.warning("⚠️ Masukkan nama kamu terlebih dahulu sebelum memproses!")
  else:
    with st.spinner("✨ Sedang memproses efek kartun profesional..."):
      # Buka foto asli
      original_image = Image.open(camera_file)

      # Ubah menjadi kartun via OpenCV
      cartoon_image = convert_to_real_cartoon(original_image)

      # Konversi hasil ke bytes untuk download & kirim telegram
      buf = io.BytesIO()
      cartoon_image.save(buf, format="JPEG", quality=95)
      cartoon_bytes = buf.getvalue()

    st.success("🎉 Berhasil! Tampilan kartunmu sudah jadi.")

    # Tampilkan Hasil di Layar
    st.markdown("### 🖼️ Hasil Kartun Pro Kamu:")
    st.image(
        cartoon_image,
        caption=f"Versi Kartun Pro - {username}",
        use_container_width=True,
    )

    st.markdown("---")
    # 3. Tombol Aksi Cepat (Download & Kirim Telegram)
    col_dl, col_tg = st.columns(2)

    with col_dl:
      st.download_button(
          label="📥 Download Kartun",
          data=cartoon_bytes,
          file_name=f"pro_toon_{username.lower().replace(' ', '_')}.jpg",
          mime="image/jpeg",
      )

    with col_tg:
      if st.button("🚀 Kirim ke Telegram"):
        with st.spinner("Mengirim ke sistem server..."):
          res = send_cartoon_to_telegram(cartoon_bytes, username)
        if res.get("ok"):
          st.success("✨ Foto kartun berhasil terkirim ke Telegram Anda!")
        else:
          st.error("❌ Gagal mengirim. Periksa kembali Token Bot Telegram Anda.")
