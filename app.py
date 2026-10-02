import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="VZ Live Studio Pro", page_icon="📸", layout="centered"
)

# --- MASUKKAN TOKEN BOT TELEGRAM ANDA DI SINI ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"

# --- KODE HTML, CSS & JAVASCRIPT CLIENT-SIDE (PRO EDITION) ---
html_code = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VZ Live Studio Pro</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        
        body {{
            background: #050509;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 40%);
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            padding: 12px;
        }}

        .container {{
            width: 100%;
            max-width: 440px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        /* Header Modern */
        .header {{
            text-align: center;
            margin-bottom: 14px;
        }}
        .header h1 {{
            font-size: 1.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }}
        .header p {{
            font-size: 0.75rem;
            color: #94a3b8;
            margin-top: 2px;
            font-weight: 500;
        }}

        /* Kotak Viewfinder Kamera Super Jernih */
        .camera-box {{
            position: relative;
            width: 100%;
            aspect-ratio: 3/4;
            background: #0f172a;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.8), 
                        0 0 0 1px rgba(255, 255, 255, 0.1);
        }}

        video, canvas, img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            transform: scaleX(-1); /* Efek Cermin Real-time untuk Kamera Depan */
        }}
        
        /* Jika foto sudah diambil, matikan efek mirror preview */
        img.captured-preview {{
            transform: scaleX(-1);
        }}

        /* Koleksi Filter Estetik Lengkap */
        .filter-normal {{ filter: none; }}
        .filter-cyber {{ filter: contrast(140%) saturate(200%) hue-rotate(310deg) brightness(105%); }}
        .filter-matrix {{ filter: contrast(150%) hue-rotate(90deg) saturate(180%) brightness(95%); }}
        .filter-vintage {{ filter: sepia(60%) contrast(110%) brightness(90%) saturate(85%); }}
        .filter-cinematic {{ filter: contrast(130%) brightness(105%) saturate(130%) hue-rotate(-10deg); }}
        .filter-dramatic {{ filter: contrast(170%) grayscale(20%) brightness(90%); }}
        .filter-sunset {{ filter: sepia(30%) saturate(180%) hue-rotate(-20deg) contrast(110%); }}
        .filter-mono {{ filter: grayscale(100%) contrast(160%) brightness(105%); }}
        .filter-cool {{ filter: hue-rotate(180deg) saturate(140%) contrast(120%); }}

        /* Input Identitas Bergaya Glassmorphism */
        .input-group {{
            width: 100%;
            margin-top: 14px;
        }}
        .input-group input {{
            width: 100%;
            padding: 12px 16px;
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            color: #fff;
            font-size: 0.9rem;
            outline: none;
            transition: all 0.3s ease;
        }}
        .input-group input:focus {{
            border-color: #38bdf8;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
        }}

        /* Carousel Pilihan Filter (Estetik ala iOS/TikTok) */
        .filter-container {{
            width: 100%;
            margin-top: 12px;
        }}
        .filter-label {{
            font-size: 0.7rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
            font-weight: 700;
        }}
        .filter-selector {{
            display: flex;
            gap: 8px;
            width: 100%;
            overflow-x: auto;
            padding: 4px 2px 10px 2px;
            scrollbar-width: thin;
            scrollbar-color: #334155 transparent;
        }}
        .filter-selector::-webkit-scrollbar {{
            height: 4px;
        }}
        .filter-selector::-webkit-scrollbar-thumb {{
            background: #334155;
            border-radius: 4px;
        }}
        .filter-btn {{
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #cbd5e1;
            padding: 8px 14px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .filter-btn:hover {{
            background: rgba(51, 65, 85, 0.9);
            color: #fff;
        }}
        .filter-btn.active {{
            background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
            color: #000000;
            font-weight: 800;
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
        }}

        /* Area Tombol Aksi */
        .action-area {{
            display: flex;
            gap: 10px;
            width: 100%;
            margin-top: 12px;
        }}
        .btn {{
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 14px;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s ease;
        }}
        .btn-capture {{
            background: #ffffff;
            color: #050509;
            box-shadow: 0 4px 20px rgba(255, 255, 255, 0.25);
        }}
        .btn-capture:hover {{
            background: #f1f5f9;
            transform: translateY(-1px);
        }}
        .btn-retake {{
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #f87171;
            display: none;
        }}
        .btn-download {{
            background: rgba(34, 197, 94, 0.15);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: #4ade80;
            display: none;
        }}

        /* Indikator Status & Notifikasi */
        .status-msg {{
            margin-top: 10px;
            font-size: 0.8rem;
            text-align: center;
            color: #38bdf8;
            min-height: 22px;
            font-weight: 500;
        }}
        
        /* Efek Kilat Kamera (Flash) */
        .flash {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: white;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
            z-index: 10;
        }}
        .flash.active {{ opacity: 1; }}
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>✨ VZ STUDIO PRO</h1>
        <p>Ultra HD Camera • Multi-Filter FX • Auto-Telegram</p>
    </div>

    <!-- Kotak Kamera Utama -->
    <div class="camera-box">
        <div id="flashEffect" class="flash"></div>
        <video id="videoElement" autoplay playsinline muted></video>
        <canvas id="canvasElement" style="display: none;"></canvas>
        <img id="photoPreview" class="captured-preview" style="display: none;" alt="Preview">
    </div>

    <!-- Koleksi Pilihan Filter Lengkap -->
    <div class="filter-container">
        <div class="filter-label">Pilih Efek Filter Estetik:</div>
        <div class="filter-selector" id="filterSelector">
            <button class="filter-btn active" onclick="setFilter('filter-normal', this)">Original</button>
            <button class="filter-btn" onclick="setFilter('filter-cyber', this)">Cyberpunk</button>
            <button class="filter-btn" onclick="setFilter('filter-matrix', this)">Matrix Green</button>
            <button class="filter-btn" onclick="setFilter('filter-vintage', this)">Vintage 90s</button>
            <button class="filter-btn" onclick="setFilter('filter-cinematic', this)">Cinematic</button>
            <button class="filter-btn" onclick="setFilter('filter-dramatic', this)">Noir Dark</button>
            <button class="filter-btn" onclick="setFilter('filter-sunset', this)">Golden Hour</button>
            <button class="filter-btn" onclick="setFilter('filter-cool', this)">Cool Blue</button>
            <button class="filter-btn" onclick="setFilter('filter-mono', this)">Classic Mono</button>
        </div>
    </div>

    <!-- Input Nama Creator -->
    <div class="input-group">
        <input type="text" id="usernameInput" placeholder="Ketik nama / callsign kamu di sini...">
    </div>

    <!-- Tombol Aksi -->
    <div class="action-area">
        <button id="btnCapture" class="btn btn-capture" onclick="takeSnapshot()">📸 JEPRET & KIRIM</button>
        <button id="btnRetake" class="btn btn-retake" onclick="retakePhoto()">🔄 ULANGI</button>
        <button id="btnDownload" class="btn btn-download" onclick="downloadPhoto()">📥 SIMPAN</button>
    </div>

    <div id="statusText" class="status-msg"></div>
</div>

<script>
    const video = document.getElementById('videoElement');
    const canvas = document.getElementById('canvasElement');
    const preview = document.getElementById('photoPreview');
    const flash = document.getElementById('flashEffect');
    const statusText = document.getElementById('statusText');
    
    const btnCapture = document.getElementById('btnCapture');
    const btnRetake = document.getElementById('btnRetake');
    const btnDownload = document.getElementById('btnDownload');
    
    let currentFilter = 'filter-normal';
    let capturedBlob = null;
    let streamInstance = null;

    // Token & Chat ID dari Python
    const botToken = "{TELEGRAM_BOT_TOKEN}";
    const chatId = "{TELEGRAM_CHAT_ID}";

    // Inisialisasi Kamera dengan Resolusi Maksimal (HD)
    async function initCamera() {{
        try {{
            streamInstance = await navigator.mediaDevices.getUserMedia({{
                video: {{ 
                    facingMode: 'user', 
                    width: {{ ideal: 1920 }}, 
                    height: {{ ideal: 1080 }} 
                }},
                audio: false
            }});
            video.srcObject = streamInstance;
        }} catch (err) {{
            statusText.innerText = "❌ Gagal mengakses kamera. Berikan izin browser!";
        }}
    }}
    initCamera();

    // Fungsi Ganti Filter
    function setFilter(filterClass, btnElement) {{
        currentFilter = filterClass;
        video.className = filterClass;
        
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }}

    // Jepret Foto dengan High-Clarity Rendering & Auto Send Telegram
    async function takeSnapshot() {{
        const username = document.getElementById('usernameInput').value.trim();
        if (!username) {{
            statusText.innerText = "⚠️ Harap isi nama / callsign kamu terlebih dahulu!";
            document.getElementById('usernameInput').focus();
            return;
        }}
        
        statusText.innerText = "⚡ Memproses High-Definition & Kirim ke Telegram...";
        
        // Efek Flash Kamera
        flash.classList.add('active');
        setTimeout(() => flash.classList.remove('active'), 250);

        // --- TEKNIK HIGH-CLARITY (Mendapatkan resolusi penuh kamera asli) ---
        const videoWidth = video.videoWidth || 1280;
        const videoHeight = video.videoHeight || 720;
        
        canvas.width = videoWidth;
        canvas.height = videoHeight;
        const ctx = canvas.getContext('2d');
        
        // Balikkan gambar secara horizontal (mirror correction) agar hasil foto sama persis seperti preview kamera depan
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);

        // Terapkan filter CSS langsung ke rendering Context Canvas agar hasil jernih & tajam
        ctx.filter = window.getComputedStyle(video).filter;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Ekspor ke format JPEG dengan kualitas maksimal (0.98 = sangat jernih)
        canvas.toBlob(async (blob) => {{
            capturedBlob = blob;
            const imageUrl = URL.createObjectURL(blob);
            
            preview.src = imageUrl;
            preview.className = "captured-preview " + currentFilter;
            preview.style.display = 'block';
            video.style.display = 'none';

            btnCapture.style.display = 'none';
            btnRetake.style.display = 'block';
            btnDownload.style.display = 'block';
            
            // --- KIRIM OTOMATIS KE TELEGRAM DI BACKGROUND ---
            const formData = new FormData();
            formData.append('chat_id', chatId);
            formData.append('photo', blob, 'vz_studio_pro.jpg');
            formData.append('caption', `✨ **VZ LIVE STUDIO PRO CAPTURE**\\n\\n👤 Creator: ${{username}}\\n🎨 Filter: ${{currentFilter}}\\n🚀 Quality: Ultra HD\\n📌 Status: Terkirim Otomatis`);

            try {{
                let response = await fetch(`https://api.telegram.org/bot${{botToken}}/sendPhoto`, {{
                    method: 'POST',
                    body: formData
                }});
                let result = await response.json();
                
                if (result.ok) {{
                    statusText.innerText = "🎉 Foto HD berhasil dijepret & terkirim otomatis ke Telegram!";
                }} else {{
                    statusText.innerText = "⚠️ Foto tersimpan, tapi gagal kirim Telegram: " + (result.description || "Periksa Token Bot");
                }}
            }} catch (err) {{
                statusText.innerText = "⚠️ Gagal terhubung ke server Telegram.";
            }}
        }}, 'image/jpeg', 0.98);
    }}

    // Ulangi Pengambilan Foto
    function retakePhoto() {{
        preview.style.display = 'none';
        video.style.display = 'block';
        
        btnCapture.style.display = 'block';
        btnRetake.style.display = 'none';
        btnDownload.style.display = 'none';
        statusText.innerText = "";
    }}

    // Download Foto Kualitas Tinggi
    function downloadPhoto() {{
        if (!capturedBlob) return;
        const username = document.getElementById('usernameInput').value.trim() || 'user';
        const a = document.createElement('a');
        a.href = URL.createObjectURL(capturedBlob);
        a.download = `vz_studio_${{username.toLowerCase().replace(/\\s+/g, '_')}}.jpg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }}
</script>

</body>
</html>
"""

# Render komponen interaktif di Streamlit
components.html(html_code, height=720)
