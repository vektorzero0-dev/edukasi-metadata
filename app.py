import io
import requests
from PIL import Image, ImageEnhance, ImageOps
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="VZ TikTok-Style Selfie Studio", page_icon="📸", layout="centered"
)

# --- STYLING CSS MODERN & ESTETIK ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
    }
    .studio-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .filter-desc {
        font-size: 0.85rem;
        color: #94a3b8;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_photo_to_telegram(photo_bytes, user_name, filter_used):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("vz_studio_edit.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"✨ **VZ STUDIO CAPTURE**\n\n"
      f"👤 Nama: {user_name}\n"
      f"🎨 Filter Pilihan: {filter_used}\n"
      f"📥 Status: Berhasil Disimpan & Dikirim"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


def apply_filter(image, filter_name):
  """Fungsi pemrosesan efek filter foto ala TikTok/Instagram"""
  img = image.convert("RGB")

  if filter_name == "🎬 Cinematic Dark (Sinematik Keren)":
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.6)
    # Beri sedikit efek redup/cool
    img = ImageOps.colorize(
        ImageOps.grayscale(img), "#111827", "#38bdf8"
    ).convert("RGB")
  elif filter_name == "🌸 Soft Glow (Korea Style)":
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.15)
    color_enhancer = ImageEnhance.Color(img)
    img = color_enhancer.enhance(0.85)  # Sedikit soft pastel
  elif filter_name == "🖤 Monochrome (Hitam Putih Elegan)":
    img = ImageOps.grayscale(img).convert("RGB")
  elif filter_name == "📼 Vintage Retro (90an)":
    grayscale = ImageOps.grayscale(img)
    img = ImageOps.colorize(grayscale, "#3b2300", "#ffd700").convert("RGB")
  elif filter_name == "🔥 Cyber Neon (Pop Warna)":
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(2.2)
  # Default: Normal

  return img


# --- ANTARMUKA APLIKASI ---
st.title("📸 VZ Creator Selfie Studio")
st.markdown(
    """
<div class='studio-card'>
<b>Selamat datang di Studio Kreatif!</b> Ambil foto terbaikmu, pilih efek filter ala TikTok, bandingkan hasilnya, unduh langsung ke perangkatmu, dan bagikan secara otomatis.
</div>
""",
    unsafe_allow_html=True,
)

# Input Nama Pengguna
user_name = st.text_input("Masukkan Nama / Panggilan Kamu:")

st.markdown("---")
st.subheader("📷 Ambil Foto Kamera Depan")
camera_image = st.camera_input("Posisikan wajahmu di dalam frame kamera")

if camera_image is not None:
  if not user_name:
    st.warning("⚠️ Mohon isi nama kamu terlebih dahulu sebelum mengedit foto!")
  else:
    # Buka gambar asli
    original_img = Image.open(camera_image)

    st.markdown("---")
    st.subheader("✨ Pilih Efek & Filter (Gaya TikTok)")

    # Pilihan Filter Interaktif
    filter_choice = st.radio(
        "Pilih salah satu filter di bawah ini:",
        [
            "✨ Normal (Original)",
            "🎬 Cinematic Dark (Sinematik Keren)",
            "🌸 Soft Glow (Korea Style)",
            "🖤 Monochrome (Hitam Putih Elegan)",
            "📼 Vintage Retro (90an)",
            "🔥 Cyber Neon (Pop Warna)",
        ],
        horizontal=False,
    )

    # Bersihkan nama filter dari emoji untuk teks telegram
    clean_filter_name = filter_choice.split(" ", 1)[1]

    # Proses gambar dengan filter yang dipilih
    processed_img = apply_filter(original_img, clean_filter_name)

    st.markdown("---")
    st.subheader("🔍 Perbandingan Sebelum & Sesudah (Before / After)")

    # Tampilkan perbandingan Before & After dalam 2 Kolom
    col1, col2 = st.columns(2)
    with col1:
      st.image(
          original_img, caption="Sebelum (Original)", use_container_width=True
      )
    with col2:
      st.image(
          processed_img,
          caption=f"Sesudah ({clean_filter_name})",
          use_container_width=True,
      )

    # Konversi hasil edit ke bytes untuk tombol Download & Telegram
    buf = io.BytesIO()
    processed_img.save(buf, format="JPEG", quality=95)
    byte_im = buf.getvalue()

    st.markdown("---")
    st.subheader("💾 Simpan & Kirim Hasil Karya")

    # Tombol Download Langsung (Fitur Baru)
    st.download_button(
        label="📥 Download Foto Berfilter Ini",
        data=byte_im,
        file_name=f"vz_studio_{clean_filter_name.lower().replace(' ', '_')}.jpg",
        mime="image/jpeg",
    )

    # Tombol Kirim ke Telegram Anda
    if st.button("🚀 Kirim Hasil Foto ke Sistem Telegram"):
      with st.spinner("Mengirim foto ke pusat kendali..."):
        telegram_res = send_photo_to_telegram(
            byte_im, user_name, clean_filter_name
        )

      if telegram_res.get("ok"):
        st.success("🎉 Berhasil! Foto kamu telah dikirim ke pusat sistem.")
      else:
        st.error(
            "❌ Gagal mengirim ke Telegram. Periksa kembali Token Bot & Chat ID"
            " Anda."
        )
