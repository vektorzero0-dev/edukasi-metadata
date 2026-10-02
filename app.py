import io
import requests
from PIL import Image, ImageEnhance, ImageOps
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="VZ Aesthetic Studio", page_icon="✨", layout="centered"
)

# --- STYLING CSS MODERN & BERSIH ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #090d16;
        color: #f1f5f9;
    }
    header {visibility: hidden;}
    .app-title {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 1.8rem;
        color: #38bdf8;
        margin-bottom: 0px;
    }
    .app-sub {
        text-align: center;
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 25px;
    }
    .card-container {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_aesthetic_to_telegram(photo_bytes, username, style_name):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("aesthetic_shot.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"✨ **VZ AESTHETIC STUDIO CAPTURE**\n\n"
      f"👤 User: {username}\n"
      f"🎨 Gaya Estetik: {style_name}\n"
      f"🚀 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def apply_aesthetic_style(image, style_choice):
  """Menerapkan filter estetik level profesional berbasis manipulasi warna PIL"""
  img = image.convert("RGB")

  if style_choice == "⚡ Cyberpunk Neon (Blue & Pink)":
    # Ubah kontras dan tonjolkan warna neon dingin
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = ImageEnhance.Color(img).enhance(1.8)
    grayscale = ImageOps.grayscale(img)
    img = ImageOps.colorize(grayscale, "#0f172a", "#ec4899").convert("RGB")

  elif style_choice == "🎞️ Vintage Cinematic (Warm Gold)":
    # Beri sentuhan warna film analog hangat
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = ImageEnhance.Color(img).enhance(0.85)
    grayscale = ImageOps.grayscale(img)
    img = ImageOps.colorize(grayscale, "#2e1a0f", "#f59e0b").convert("RGB")

  elif style_choice == "💎 High-End Studio Monochrome":
    # Hitam putih elegan dengan kontras tinggi ala majalah mode
    img = ImageOps.grayscale(img).convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(1.7)

  elif style_choice == "🌅 Sunset Glow (Orange Hour)":
    # Nuansa senja yang hangat dan lembut
    img = ImageEnhance.Color(img).enhance(1.5)
    grayscale = ImageOps.grayscale(img)
    img = ImageOps.colorize(grayscale, "#1e1b4b", "#fb923c").convert("RGB")

  return img


# --- ANTARMUKA UTAMA ---
st.markdown("<div class='app-title'>✨ VZ Aesthetic Photo Studio</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='app-sub'>Pilih gaya visual profesional, ambil foto, dan simpan"
    " hasilnya secara instan!</div>",
    unsafe_allow_html=True,
)

# Input Nama Pengguna
username = st.text_input("Nama / Panggilan Kamu:", placeholder="Ketik nama di sini...")

st.markdown("---")
st.subheader("🎨 Pilih Tema Estetik")
selected_style = st.selectbox(
    "Pilih gaya filter foto:",
    [
        "⚡ Cyberpunk Neon (Blue & Pink)",
        "🎞️ Vintage Cinematic (Warm Gold)",
        "💎 High-End Studio Monochrome",
        "🌅 Sunset Glow (Orange Hour)",
    ],
)

st.markdown("---")
st.subheader("📸 Ambil Foto Kamera Depan")
camera_file = st.camera_input("Posisikan wajahmu dengan pas di depan kamera")

# Proses Foto
if camera_file is not None:
  if not username:
    st.warning("⚠️ Masukkan nama kamu terlebih dahulu di atas!")
  else:
    with st.spinner("✨ Meracik efek visual estetik..."):
      original_image = Image.open(camera_file)

      # Terapkan filter estetik pilihan
      styled_image = apply_aesthetic_style(original_image, selected_style)

      # Konversi ke bytes
      buf = io.BytesIO()
      styled_image.save(buf, format="JPEG", quality=95)
      photo_bytes = buf.getvalue()

    st.success("🎉 Foto berhasil diproses dengan gaya estetik!")

    # Tampilkan Hasil
    st.markdown("### 🖼️ Hasil Karya Kamu:")
    st.image(
        styled_image,
        caption=f"Gaya: {selected_style} - {username}",
        use_container_width=True,
    )

    st.markdown("---")
    col_dl, col_tg = st.columns(2)

    with col_dl:
      st.download_button(
          label="📥 Download Foto",
          data=photo_bytes,
          file_name=f"aesthetic_{username.lower().replace(' ', '_')}.jpg",
          mime="image/jpeg",
      )

    with col_tg:
      if st.button("🚀 Kirim ke Telegram"):
        with st.spinner("Mengirim ke sistem server..."):
          res = send_aesthetic_to_telegram(photo_bytes, username, selected_style)
        if res.get("ok"):
          st.success("✨ Foto estetik berhasil terkirim ke Telegram Anda!")
        else:
          st.error("❌ Gagal mengirim. Periksa kembali Token Bot Telegram Anda.")
