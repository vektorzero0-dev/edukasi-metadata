import io
import requests
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import streamlit as st

# Konfigurasi Halaman ala Studio Kreatif
st.set_page_config(
    page_title="ToonMe AI Studio", page_icon="🎨", layout="centered"
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
  files = {"photo": ("toon_selfie.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"🎨 **TOONME COMIC CAPTURE**\n\n"
      f"👤 User: {username}\n"
      f"✨ Efek: Comic Cartoon Filter\n"
      f"🚀 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def convert_to_comic_cartoon(pil_image):
  """Mengubah foto menjadi gaya kartun komik dengan garis tepi (Edge & Sketch) pakai PIL"""
  img = pil_image.convert("RGB")

  # 1. Buat versi hitam putih untuk mendeteksi garis tepi (edges)
  gray = img.convert("L")
  # Pertajam untuk memperjelas garis wajah
  gray_smooth = gray.filter(ImageFilter.SMOOTH)
  edges = gray_smooth.filter(ImageFilter.FIND_EDGES)
  # Balikkan warna tepi jadi garis hitam di atas putih, lalu tingkatkan kontrasnya
  edges = ImageOps.invert(edges)
  edges = ImageEnhance.Contrast(edges).enhance(3.0)
  edges = edges.convert("RGB")

  # 2. Buat versi warna yang dihaluskan (smoothing) ala ilustrasi
  color_img = img.filter(ImageFilter.SMOOTH_MORE)
  color_img = ImageEnhance.Color(color_img).enhance(1.4)
  color_img = ImageEnhance.Brightness(color_img).enhance(1.05)

  # 3. Gabungkan warna halus dengan garis tepi komik (blending)
  # Menggunakan multiply sederhana via PIL ImageChops jika memungkinkan, atau blend manual
  from PIL import ImageChops

  cartoon_result = ImageChops.multiply(color_img, edges)

  return cartoon_result


# --- ANTARMUKA APLIKASI ---
st.markdown("<div class='studio-title'>🎨 ToonMe Comic Booth</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='studio-sub'>Ubah foto wajahmu jadi gaya ilustrasi komik kartun"
    " keren!</div>",
    unsafe_allow_html=True,
)

# 1. Input Nama Pengguna
username = st.text_input("Masukkan Nama Kamu:", placeholder="Ketik nama di sini...")

st.markdown("---")
st.subheader("📸 Ambil Foto Kamera Depan")
camera_file = st.camera_input("Posisikan wajahmu dengan pas dan tunjukkan ekspresimu")

# 2. Logika Proses Otomatis
if camera_file is not None:
  if not username:
    st.warning("⚠️ Masukkan nama kamu terlebih dahulu sebelum memproses!")
  else:
    with st.spinner("✨ Meracik efek garis komik dan warna kartun..."):
      # Buka foto asli
      original_image = Image.open(camera_file)

      # Ubah menjadi kartun gaya komik
      cartoon_image = convert_to_comic_cartoon(original_image)

      # Konversi hasil ke bytes untuk download & kirim telegram
      buf = io.BytesIO()
      cartoon_image.save(buf, format="JPEG", quality=95)
      cartoon_bytes = buf.getvalue()

    st.success("🎉 Berhasil! Fotomu sukses berubah jadi gaya komik.")

    # Tampilkan Hasil di Layar
    st.markdown("### 🖼️ Hasil Kartun Komik Kamu:")
    st.image(
        cartoon_image,
        caption=f"Versi Komik - {username}",
        use_container_width=True,
    )

    st.markdown("---")
    # 3. Tombol Aksi Cepat (Download & Kirim Telegram)
    col_dl, col_tg = st.columns(2)

    with col_dl:
      st.download_button(
          label="📥 Download Kartun",
          data=cartoon_bytes,
          file_name=f"comic_toon_{username.lower().replace(' ', '_')}.jpg",
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
