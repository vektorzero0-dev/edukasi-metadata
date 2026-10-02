from datetime import datetime
import io
import requests
from PIL import Image, ImageEnhance, ImageOps
import streamlit as st

# Konfigurasi Halaman (Full-screen cinematic feel)
st.set_page_config(
    page_title="Viewfinder Camera Studio", page_icon="📷", layout="centered"
)

# --- STYLING CSS SENSASI KAMERA PROFESIONAL ---
st.markdown(
    """
    <style>
    /* Latar Belakang Gelap Total ala Studio / Darkroom */
    .stApp {
        background-color: #050505;
        color: #f8fafc;
        font-family: 'Courier New', Courier, monospace; /* Memberikan kesan digital/kamera */
    }
    header {visibility: hidden;}
    
    /* Panel Viewfinder Kamera */
    .camera-hud {
        border: 2px solid rgba(255, 255, 255, 0.2);
        background-color: #0b0f19;
        padding: 15px;
        border-radius: 8px;
        position: relative;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.8);
    }
    
    /* Indikator HUD ala Kamera Profesional */
    .hud-top {
        display: flex;
        justify-content: space-between;
        font-size: 0.75rem;
        color: #38bdf8;
        letter-spacing: 2px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    .hud-rec {
        color: #ef4444;
        animation: blink 1.5s infinite;
    }
    
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }
    
    /* Gaya Tombol Aksi */
    .stButton>button {
        width: 100%;
        background-color: #ffffff;
        color: #000000;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        letter-spacing: 1px;
        padding: 12px;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #38bdf8;
        color: #000000;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_to_telegram(photo_bytes, username, lens_mode):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("studio_capture.jpg", photo_bytes, "image/jpeg")}
  current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
  caption = (
      f"📷 **VIEWFINDER STUDIO CAPTURE**\n\n"
      f"👤 Operator: {username}\n"
      f"⚡ Mode: {lens_mode}\n"
      f"🕒 Waktu: {current_time}\n"
      f"🚀 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def apply_studio_tone(image, mode):
  """Penyempurnaan warna khas lensa kamera sinema"""
  img = image.convert("RGB")
  if mode == "🎬 Cinema Prime (Anamorphic Look)":
    img = ImageEnhance.Contrast(img).enhance(1.2)
    img = ImageEnhance.Color(img).enhance(1.15)
    img = ImageEnhance.Sharpness(img).enhance(1.4)
  elif mode == "💎 Studio Portrait Clean":
    img = ImageEnhance.Brightness(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.5)
  elif mode == "🎞️ Vintage Analog Grade":
    img = ImageEnhance.Color(img).enhance(0.8)
    grayscale = ImageOps.grayscale(img)
    img = ImageOps.colorize(grayscale, "#1a120b", "#e09f3e").convert("RGB")
  return img


# --- TAMPILAN UTAMA (HUD LAYOUT) ---
st.markdown(
    """
<div class="camera-hud">
    <div class="hud-top">
        <span>ISO 400 &nbsp;|&nbsp; f/2.8 &nbsp;|&nbsp; 1/250s</span>
        <span class="hud-rec">● REC [LIVE VIEW]</span>
    </div>
""",
    unsafe_allow_html=True,
)

st.title("📷 VZ-01 CAMERA STUDIO")
st.markdown(
    "<p style='color: #94a3b8; font-size: 0.85rem; margin-top: -10px;'>Sistem"
    " Jendela Bidik Digital & Integrasi Otomatis</p>",
    unsafe_allow_html=True,
)

# Input Operator / Pengguna
username = st.text_input("IDENTITAS OPERATOR:", placeholder="Masukkan nama...")

# Pilihan Lensa / Mode Tangkap
lens_mode = st.selectbox(
    "PILIHAN PROFIL LENSA:",
    [
        "🎬 Cinema Prime (Anamorphic Look)",
        "💎 Studio Portrait Clean",
        "🎞️ Vintage Analog Grade",
    ],
)

st.markdown("---")
st.markdown("### 🔴 BIDIK KAMERA UTAMA")
camera_file = st.camera_input("Ambil gambar melalui sensor aktif")

st.markdown("</div>", unsafe_allow_html=True)  # Tutup wadah HUD

# Logika Pemrosesan Gambar
if camera_file is not None:
  if not username:
    st.warning("⚠️ MASUKKAN IDENTITAS OPERATOR TERLEBIH DAHULU!")
  else:
    with st.spinner("MENGEKSEKUSI FRAME KAMERA..."):
      raw_image = Image.open(camera_file)
      processed_image = apply_studio_tone(raw_image, lens_mode)

      buf = io.BytesIO()
      processed_image.save(buf, format="JPEG", quality=95)
      photo_bytes = buf.getvalue()

    st.success("✨ FRAME BERHASIL DIREKAM!")

    # Preview Hasil
    st.markdown("### 🖼️ PREVIEW HASIL BIDIKAN:")
    st.image(
        processed_image,
        caption=f"Operator: {username} | Profil: {lens_mode}",
        use_container_width=True,
    )

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
      st.download_button(
          label="📥 UNDUH FILE",
          data=photo_bytes,
          file_name=f"vz_shot_{username.lower().replace(' ', '_')}.jpg",
          mime="image/jpeg",
      )

    with col2:
      if st.button("🚀 KIRIM KE SERVER"):
        with st.spinner("MENGIRIM DATA..."):
          res = send_to_telegram(photo_bytes, username, lens_mode)
        if res.get("ok"):
          st.success("🎉 PENGIRIMAN BERHASIL!")
        else:
          st.error("❌ PENGIRIMAN GAGAL. PERIKSA KONEKSI/TOKEN.")
