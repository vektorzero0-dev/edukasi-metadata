import io
import requests
from PIL import Image, ImageEnhance, ImageOps
import streamlit as st

# Konfigurasi Halaman (Clean iOS style)
st.set_page_config(
    page_title="iOS Camera Studio", page_icon="📸", layout="centered"
)

# --- STYLING CSS ALA KAMERA IPHONE (iOS) ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    header {visibility: hidden;}
    
    /* Header Ala iOS */
    .ios-header {
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        color: #f5f5f7;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .ios-sub {
        text-align: center;
        font-size: 0.8rem;
        color: #86868b;
        margin-bottom: 20px;
    }
    
    /* Tombol Aksi Khas iOS (Clean Rounded) */
    .stButton>button {
        width: 100%;
        background-color: #0071e3; /* Apple Blue */
        color: white;
        border: none;
        border-radius: 20px;
        font-weight: 500;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #0077ed;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_iphone_shot_to_telegram(photo_bytes, username, lens_style):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("iphone_capture.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"📸 **IPHONE CAMERA CAPTURE**\n\n"
      f"👤 Pengguna: {username}\n"
      f"📷 Gaya Lensa: {lens_style}\n"
      f"🚀 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def apply_iphone_lens_style(image, style_name):
  """Menerapkan tone warna khas kamera iPhone (Natural & Clean)"""
  img = image.convert("RGB")

  if style_name == "📸 Original (True Tone)":
    # Tone asli dengan sedikit peningkatan ketajaman warna natural
    img = ImageEnhance.Color(img).enhance(1.05)
  elif style_name == "☀️ Vivid (Cerah & Kontras)":
    # Mirip mode Vivid iPhone yang pop-up dan cerah
    img = ImageEnhance.Contrast(img).enhance(1.2)
    img = ImageEnhance.Color(img).enhance(1.3)
  elif style_name == "🌅 Warm (Tone Hangat / Golden Hour)":
    # Tone hangat natural ala potret studio iPhone
    img = ImageEnhance.Color(img).enhance(1.1)
    grayscale = ImageOps.grayscale(img)
    img = ImageOps.colorize(grayscale, "#1a1105", "#ffb703").convert("RGB")
  elif style_name == "🖤 Mono (Hitam Putih Klasik)":
    # Hitam putih bersih ala kamera portrait Apple
    img = ImageOps.grayscale(img).convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(1.3)

  return img


# --- ANTARMUKA UTAMA ---
st.markdown("<div class='ios-header'>Camera Studio (iOS Style)</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='ios-sub'>Ambil foto dengan gaya lensa natural khas iPhone</div>",
    unsafe_allow_html=True,
)

# 1. Input Nama Pengguna
username = st.text_input("Nama Pengguna:", placeholder="Ketik nama kamu di sini...")

st.markdown("---")
st.subheader("⚙️ Pilih Gaya Lensa (Photos Style)")
selected_lens = st.selectbox(
    "Gaya Tone Kamera:",
    [
        "📸 Original (True Tone)",
        "☀️ Vivid (Cerah & Kontras)",
        "🌅 Warm (Tone Hangat / Golden Hour)",
        "🖤 Mono (Hitam Putih Klasik)",
    ],
)

st.markdown("---")
st.subheader("📷 Bidik Kamera Depan")
camera_file = st.camera_input("Posisikan wajahmu dengan pas di dalam frame")

# 2. Logika Pemrosesan Foto
if camera_file is not None:
  if not username:
    st.warning("⚠️ Masukkan nama kamu terlebih dahulu di atas!")
  else:
    with st.spinner("Memproses foto dengan tone iOS..."):
      original_image = Image.open(camera_file)

      # Terapkan gaya lensa iPhone
      processed_image = apply_iphone_lens_style(original_image, selected_lens)

      # Konversi ke bytes
      buf = io.BytesIO()
      processed_image.save(buf, format="JPEG", quality=95)
      photo_bytes = buf.getvalue()

    st.success("✨ Foto berhasil dijepret dan diproses!")

    # Tampilkan Hasil di Layar
    st.markdown("### 🖼️ Hasil Jepretan Kamera:")
    st.image(
        processed_image,
        caption=f"Mode: {selected_lens} - {username}",
        use_container_width=True,
    )

    st.markdown("---")
    # Tombol Aksi (Download & Telegram)
    col_dl, col_tg = st.columns(2)

    with col_dl:
      st.download_button(
          label="📥 Simpan ke Perangkat",
          data=photo_bytes,
          file_name=f"iphone_shot_{username.lower().replace(' ', '_')}.jpg",
          mime="image/jpeg",
      )

    with col_tg:
      if st.button("🚀 Kirim ke Telegram"):
        with st.spinner("Mengirim ke pusat sistem..."):
          res = send_iphone_shot_to_telegram(photo_bytes, username, selected_lens)
        if res.get("ok"):
          st.success("🎉 Foto berhasil terkirim ke Telegram Anda!")
        else:
          st.error("❌ Gagal mengirim. Periksa kembali Token Bot Telegram Anda.")
