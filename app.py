import io
import requests
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="iPhone-Grade Clarity Studio", page_icon="📸", layout="centered"
)

# --- STYLING CSS ELEGAN ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
    }
    header {visibility: hidden;}
    .studio-header {
        text-align: center;
        font-weight: 600;
        font-size: 1.4rem;
        color: #f5f5f7;
        margin-bottom: 5px;
    }
    .studio-sub {
        text-align: center;
        font-size: 0.85rem;
        color: #86868b;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        background-color: #0071e3;
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


def send_to_telegram(photo_bytes, username, mode_name):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("iphone_clear_shot.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"📸 **IPHONE-GRADE HD CAPTURE**\n\n"
      f"👤 User: {username}\n"
      f"✨ Mode Kejernihan: {mode_name}\n"
      f"🚀 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def apply_iphone_clarity_pipeline(image, mode):
  """Algoritma pemrosesan gambar agar setajam dan sejernih kamera iPhone"""
  img = image.convert("RGB")

  if mode == "💎 Ultra Retina Clear (Tajam & Jernih)":
    # 1. Tingkatkan kecerahan sedikit agar wajah lebih terang natural
    img = ImageEnhance.Brightness(img).enhance(1.08)
    # 2. Tingkatkan kontras agar detail lebih tegas
    img = ImageEnhance.Contrast(img).enhance(1.15)
    # 3. Pertajam detail wajah (Sharpness ala Apple Deep Fusion)
    img = ImageEnhance.Sharpness(img).enhance(1.8)
    # 4. Optimalkan saturasi warna
    img = ImageEnhance.Color(img).enhance(1.1)

  elif mode == "☀️ Portrait Glow (Cerah & Mulus Alami)":
    # 1. Mode Portrait: Sedikit soft focus pada latar belakang/kulit, tapi tetap tajam di detail utama
    img = ImageEnhance.Brightness(img).enhance(1.12)
    img = ImageEnhance.Color(img).enhance(1.05)
    # Berikan sedikit efek halus (smoothing) tipis untuk menghilangkan bintik noise kamera
    img = img.filter(ImageFilter.SMOOTH)
    # Pertajam kembali bagian detail mata/bibir
    img = ImageEnhance.Sharpness(img).enhance(1.4)

  elif mode == "🌅 Cinematic HDR (Kontras Dinamis Tinggi)":
    # Menyerupai hasil jepretan HDR iPhone dengan rentang dinamis tinggi
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.25)
    img = ImageEnhance.Sharpness(img).enhance(1.6)

  return img


# --- ANTARMUKA APLIKASI ---
st.markdown("<div class='studio-header'>iPhone-Grade Camera Studio</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='studio-sub'>Hasil jepretan kamera web diproses otomatis menjadi"
    " setajam dan sejernih lensa iPhone</div>",
    unsafe_allow_html=True,
)

# Input Nama
username = st.text_input("Nama Pengguna:", placeholder="Ketik nama kamu di sini...")

st.markdown("---")
st.subheader("⚙️ Pilih Engine Kejernihan Lensa")
clarity_mode = st.selectbox(
    "Mode Pemrosesan HD:",
    [
        "💎 Ultra Retina Clear (Tajam & Jernih)",
        "☀️ Portrait Glow (Cerah & Mulus Alami)",
        "🌅 Cinematic HDR (Kontras Dinamis Tinggi)",
    ],
)

st.markdown("---")
st.subheader("📸 Ambil Foto")
camera_file = st.camera_input("Posisikan wajahmu dengan pas di depan kamera")

# Logika Pemrosesan
if camera_file is not None:
  if not username:
    st.warning("⚠️ Masukkan nama kamu terlebih dahulu di atas!")
  else:
    with st.spinner("Memproses kejernihan foto ala mesin Apple..."):
      raw_image = Image.open(camera_file)

      # Terapkan pipeline kejernihan tinggi
      hd_image = apply_iphone_clarity_pipeline(raw_image, clarity_mode)

      # Konversi ke bytes berkualitas tinggi (Quality 95)
      buf = io.BytesIO()
      hd_image.save(buf, format="JPEG", quality=95)
      hd_bytes = buf.getvalue()

    st.success("✨ Foto berhasil dijernihkan!")

    # Tampilkan Hasil di Layar
    st.markdown("### 🖼️ Hasil Jepretan HD Kamu:")
    st.image(
        hd_image,
        caption=f"Mode: {clarity_mode} - {username}",
        use_container_width=True,
    )

    st.markdown("---")
    # Tombol Aksi (Download & Telegram)
    col_dl, col_tg = st.columns(2)

    with col_dl:
      st.download_button(
          label="📥 Simpan Foto HD",
          data=hd_bytes,
          file_name=f"iphone_hd_{username.lower().replace(' ', '_')}.jpg",
          mime="image/jpeg",
      )

    with col_tg:
      if st.button("🚀 Kirim ke Telegram"):
        with st.spinner("Mengirim ke pusat sistem..."):
          res = send_to_telegram(hd_bytes, username, clarity_mode)
        if res.get("ok"):
          st.success("🎉 Foto HD berhasil terkirim ke Telegram Anda!")
        else:
          st.error("❌ Gagal mengirim. Periksa kembali Token Bot Telegram Anda.")
