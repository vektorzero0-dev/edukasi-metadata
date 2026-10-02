import io
import requests
from PIL import Image, ImageEnhance, ImageOps
import streamlit as st

# Konfigurasi Halaman (Lebar pas untuk tampilan mobile/app feel)
st.set_page_config(
    page_title="TikTok Style Camera Studio", page_icon="🎵", layout="centered"
)

# --- STYLING CSS ALA TIKTOK INTERFACE ---
st.markdown(
    """
    <style>
    /* Tema Gelap Total ala Layar Kamera TikTok */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Sembunyikan elemen header default Streamlit agar bersih */
    header {visibility: hidden;}
    
    /* Judul ala Header TikTok */
    .tiktok-header {
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 5px;
    }
    
    .tiktok-sub {
        text-align: center;
        font-size: 0.85rem;
        color: #8a8b91;
        margin-bottom: 20px;
    }

    /* Kotak Kontainer Utama */
    .element-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Tombol Kustom */
    .stButton>button {
        width: 100%;
        background-color: #fe2c55; /* Warna Merah/Pink Khas TikTok */
        color: white;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #e41e45;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_to_telegram(photo_bytes, username, filter_name):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("tiktok_capture.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"🎵 **TIKTOK STUDIO CAPTURE**\n\n"
      f"👤 User: {username}\n"
      f"🎨 Filter: {filter_name}\n"
      f"🚀 Status: Terkirim Otomatis"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def apply_tiktok_filter(image, filter_type):
  img = image.convert("RGB")
  if filter_type == "✨ Glow Smooth (Beauty)":
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.12)
  elif filter_type == "🎬 Cinematic Dark":
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
  elif filter_type == "🖤 B&W Aesthetic":
    img = ImageOps.grayscale(img).convert("RGB")
  elif filter_type == "🔥 Vivid Pop":
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(2.0)
  return img


# --- TAMPILAN ANTARMUKA UTAMA ---
st.markdown("<div class='tiktok-header'>TikTok Effect Studio</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='tiktok-sub'>Pilih filter, ambil foto, download, atau kirim"
    " instan</div>",
    unsafe_allow_html=True,
)

# 1. Input Nama / ID Pengguna (Simpel di atas)
username = st.text_input("Username / Nama Kamu", placeholder="Ketik nama kamu...")

# 2. Pilihan Filter (Disajikan horizontal / pilihan cepat)
filter_option = st.selectbox(
    "🎨 Pilih Efek Filter",
    [
        "✨ Normal (Original)",
        "✨ Glow Smooth (Beauty)",
        "🎬 Cinematic Dark",
        "🖤 B&W Aesthetic",
        "🔥 Vivid Pop",
    ],
)

st.markdown("---")

# 3. Kotak Kamera Utama (Fokus ke tengah ala layar perekaman)
camera_file = st.camera_input("Ketuk untuk ambil foto")

# 4. Logika Jika Foto Sudah Diambil
if camera_file is not None:
  if not username:
    st.warning("⚠️ Masukkan username terlebih dahulu di atas!")
  else:
    # Proses Gambar
    raw_image = Image.open(camera_file)
    clean_filter_name = filter_option.split(" ", 1)[-1]
    processed_image = apply_tiktok_filter(raw_image, filter_option)

    # Konversi ke bytes
    img_bytes_io = io.BytesIO()
    processed_image.save(img_bytes_io, format="JPEG", quality=95)
    img_bytes = img_bytes_io.getvalue()

    # Tampilkan Hasil di Layar
    st.image(processed_image, use_container_width=True)

    # 5. Tombol Aksi Cepat (Model Tombol Berjajar ala TikTok Action Bar)
    col_dl, col_tg = st.columns(2)

    with col_dl:
      st.download_button(
          label="📥 Simpan",
          data=img_bytes,
          file_name=f"tiktok_snap_{username}.jpg",
          mime="image/jpeg",
      )

    with col_tg:
      if st.button("🚀 Kirim"):
        with st.spinner("Mengirim..."):
          res = send_to_telegram(img_bytes, username, clean_filter_name)
        if res.get("ok"):
          st.success("Berhasil terkirim!")
        else:
          st.error("Gagal kirim ke Telegram.")
