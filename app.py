import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="VZ iPhone Studio Pro", page_icon="📸", layout="centered"
)

# --- MASUKKAN TOKEN BOT TELEGRAM ANDA DI SINI ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"

# --- KODE HTML, CSS & JAVASCRIPT (FIXED LAYOUT & TEXT CUTTING) ---
html_code = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VZ iPhone Studio</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        
        body {{
            background: #000000;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            padding: 8px;
        }}

        .container {{
            width: 100%;
            max-width: 460px; /* Diperluas agar muat di layar sempit */
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .header {{
            text-align: center;
            margin-bottom: 8px;
            width: 100%;
        }}
        .header h1 {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #f1f5f9;
            white-space: nowrap;
        }}
        .header p {{
            font-size: 0.68rem;
            color: #94a3b8;
            margin-top: 2px;
        }}

        /* Kotak Viewfinder Kamera */
        .camera-box {{
            position: relative;
            width: 100%;
            aspect-ratio: 4/5; /* Rasio lebih proporsional untuk HP */
            background: #111;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0,0,0,0.8);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }}

        video, canvas, img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            transform: scaleX(-1);
        }}
        
        img.captured-preview {{
            transform: scaleX(-1);
        }}

        /* Preset Engine Filter */
        .mode-iphone {{ filter: brightness(1.08) contrast(1.12) saturate(1.15); }}
        .mode-hdr {{ filter: brightness(1.05) contrast(1.22) saturate(1.20); }}
        .mode-portrait {{ filter: brightness(1.12) contrast(1.08) saturate(1.25) sepia(0.1); }}
        .mode-bright {{ filter: brightness(1.20) contrast(1.05) saturate(1.10); }}
        .mode-raw {{ filter: none; }}

        /* Pilihan Engine / Filter */
        .filter-container {{
            width: 100%;
            margin-top: 8px;
        }}
        .filter-label {{
            font-size: 0.62rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 4px;
            font-weight: 700;
        }}
        .filter-selector {{
            display: flex;
            gap: 6px;
            width: 100%;
            overflow-x: auto;
            padding: 2px 2px 6px 2px;
            scrollbar-width: none;
        }}
        .filter-selector::-webkit-scrollbar {{ display: none; }}
        
        .filter-btn {{
            background: #161b22;
            border: 1px solid #30363d;
            color: #8b949e;
            padding: 7px 12px;
            border-radius: 12px;
            font-size: 0.72rem;
            font-weight: 600;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .filter-btn.active {{
            background: #ffffff;
            color: #000000;
            font-weight: 700;
            border-color: #ffffff;
        }}

        /* Input Nama */
        .input-group {{
            width: 100%;
            margin-top: 8px;
        }}
        .input-group input {{
            width: 100%;
            padding: 10px 14px;
            background: #111622;
            border: 1px solid #2a3447;
            border-radius: 12px;
            color: #fff;
            font-size: 0.82rem;
            outline: none;
        }}
        .input-group input:focus {{ border-color: #3b82f6; }}

        /* Tombol Aksi */
        .action-area {{
            display: flex;
            gap: 8px;
            width: 100%;
            margin-top: 8px;
        }}
        .btn {{
            flex: 1;
            padding: 11px;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.82rem;
            cursor: pointer;
            text-align: center;
        }}
        .btn-capture {{ background: #ffffff; color: #000000; }}
        .btn-retake {{ background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.3); color: #f87171; display: none; }}
        .btn-download {{ background: rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.3); color: #4ade80; display: none; }}

        .status-msg {{
            margin-top: 6px;
            font-size: 0.72rem;
            text-align: center;
            color: #38bdf8;
            min-height: 18px;
            font-weight: 500;
        }}
        
        .flash {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: white;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.15s ease;
            z-index: 10;
        }}
        .flash.active {{ opacity: 1; }}
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>📸 VZ IPHONE STUDIO</h1>
        <p>Real-Time Engine • Auto Telegram</p>
    </div>

    <!-- Kotak Kamera -->
    <div class="camera-box">
        <div id="flashEffect" class="flash"></div>
        <video id="videoElement" class="mode-iphone" autoplay playsinline muted></video>
        <canvas id="canvasElement" style="display: none;"></canvas>
        <img id="photoPreview" class="captured-preview mode-iphone" style="display: none;" alt="Preview">
    </div>

    <!-- Pilihan Engine / Filter -->
    <div class="filter-container">
        <div class="filter-label">Pilih Engine Kamera:</div>
        <div class="filter-selector" id="filterSelector">
            <button class="filter-btn active" onclick="setMode('mode-iphone', this)">iPhone Natural</button>
            <button class="filter-btn" onclick="setMode('mode-hdr', this)">Smart HDR</button>
            <button class="filter-btn" onclick="setMode('mode-portrait', this)">Warm Portrait</button>
            <button class="filter-btn" onclick="setMode('mode-bright', this)">Clean Studio</button>
            <button class="filter-btn" onclick="setMode('mode-raw', this)">RAW Original</button>
        </div>
    </div>

    <!-- Input Nama -->
    <div class="input-group">
        <input type="text" id="usernameInput" placeholder="Ketik nama / callsign kamu...">
    </div>

    <!-- Tombol Aksi -->
    <div class="action-area">
        <button id="btnCapture" class="btn btn-capture" onclick="takeSnapshot()">📸 AMBIL & KIRIM</button>
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
    
    let currentModeClass = 'mode-iphone';
    let capturedBlob = null;
    let streamInstance = null;

    const botToken = "{TELEGRAM_BOT_TOKEN}";
    const chatId = "{TELEGRAM_CHAT_ID}";

    async function initCamera() {{
        try {{
            streamInstance = await navigator.mediaDevices.getUserMedia({{
                video: {{ facingMode: 'user', width: {{ ideal: 1280 }}, height: {{ ideal: 720 }} }},
                audio: false
            }});
            video.srcObject = streamInstance;
        }} catch (err) {{
            statusText.innerText = "❌ Gagal akses kamera. Izinkan browser!";
        }}
    }}
    initCamera();

    function setMode(modeClass, btnElement) {{
        currentModeClass = modeClass;
        video.className = modeClass;
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }}

    async function takeSnapshot() {{
        const username = document.getElementById('usernameInput').value.trim();
        if (!username) {{
            statusText.innerText = "⚠️ Harap isi nama / callsign kamu dulu!";
            document.getElementById('usernameInput').focus();
            return;
        }}
        
        statusText.innerText = "⚡ Mengambil foto & Kirim ke Telegram...";
        
        flash.classList.add('active');
        setTimeout(() => flash.classList.remove('active'), 200);

        canvas.width = video.videoWidth || 1280;
        canvas.height = video.videoHeight || 720;
        const ctx = canvas.getContext('2d');
        
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        ctx.filter = window.getComputedStyle(video).filter;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(async (blob) => {{
            capturedBlob = blob;
            preview.src = URL.createObjectURL(blob);
            preview.className = "captured-preview " + currentModeClass;
            preview.style.display = 'block';
            video.style.display = 'none';

            btnCapture.style.display = 'none';
            btnRetake.style.display = 'block';
            btnDownload.style.display = 'block';
            
            const formData = new FormData();
            formData.append('chat_id', chatId);
            formData.append('photo', blob, 'iphone_studio.jpg');
            formData.append('caption', `✨ **VZ IPHONE STUDIO**\\n\\n👤 Creator: ${{username}}\\n⚙️ Engine: ${{currentModeClass.replace('mode-', '').toUpperCase()}}\\n🚀 Status: Terkirim Otomatis`);

            try {{
                let response = await fetch(`https://api.telegram.org/bot${{botToken}}/sendPhoto`, {{
                    method: 'POST',
                    body: formData
                }});
                let result = await response.json();
                
                if (result.ok) {{
                    statusText.innerText = "🎉 Foto terkirim otomatis ke Telegram!";
                }} else {{
                    statusText.innerText = "⚠️ Gagal kirim Telegram: " + (result.description || "Cek Token");
                }}
            }} catch (err) {{
                statusText.innerText = "⚠️ Koneksi Telegram bermasalah.";
            }}
        }}, 'image/jpeg', 0.95);
    }}

    function retakePhoto() {{
        preview.style.display = 'none';
        video.style.display = 'block';
        btnCapture.style.display = 'block';
        btnRetake.style.display = 'none';
        btnDownload.style.display = 'none';
        statusText.innerText = "";
    }}

    function downloadPhoto() {{
        if (!capturedBlob) return;
        const username = document.getElementById('usernameInput').value.trim() || 'user';
        const a = document.createElement('a');
        a.href = URL.createObjectURL(capturedBlob);
        a.download = `vz_iphone_${{username.toLowerCase().replace(/\\s+/g, '_')}}.jpg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }}
</script>

</body>
</html>
"""

# Render komponen interaktif dengan tinggi iframe yang disesuaikan agar tidak terpotong
components.html(html_code, height=660)
