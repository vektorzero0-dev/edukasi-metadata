import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="VZ Live Camera Studio", page_icon="📸", layout="centered"
)

# --- MASUKKAN TOKEN BOT TELEGRAM ANDA DI SINI ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"

# --- KODE HTML, CSS & JAVASCRIPT CLIENT-SIDE (TIKTOK/IG STYLE) ---
html_code = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VZ Live Camera</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        body {{
            background-color: #000000;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            padding: 10px;
        }}
        .container {{
            width: 100%;
            max-width: 420px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .header {{
            text-align: center;
            margin-bottom: 12px;
        }}
        .header h1 {{
            font-size: 1.2rem;
            font-weight: 700;
            color: #f8fafc;
        }}
        .header p {{
            font-size: 0.75rem;
            color: #94a3b8;
        }}
        
        /* Area Viewfinder Kamera */
        .camera-box {{
            position: relative;
            width: 100%;
            aspect-ratio: 3/4;
            background: #111;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(0,0,0,0.7);
            border: 1px solid rgba(255,255,255,0.15);
        }}
        video, canvas, img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
        }}
        
        /* Efek Filter CSS Real-Time */
        .filter-normal {{ filter: none; }}
        .filter-cyber {{ filter: contrast(130%) saturate(180%) hue-rotate(330deg); }}
        .filter-vintage {{ filter: sepia(50%) contrast(110%) brightness(95%) saturate(90%); }}
        .filter-cinematic {{ filter: contrast(125%) brightness(105%) saturate(120%); }}
        .filter-mono {{ filter: grayscale(100%) contrast(140%); }}
        
        /* Input Nama */
        .input-group {{
            width: 100%;
            margin-top: 12px;
        }}
        .input-group input {{
            width: 100%;
            padding: 10px 14px;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            color: #fff;
            font-size: 0.9rem;
            outline: none;
        }}
        .input-group input:focus {{
            border-color: #38bdf8;
        }}

        /* Pilihan Filter (Horizonal Scroll ala TikTok) */
        .filter-selector {{
            display: flex;
            gap: 8px;
            width: 100%;
            overflow-x: auto;
            padding: 10px 0;
            scrollbar-width: none;
        }}
        .filter-selector::-webkit-scrollbar {{ display: none; }}
        .filter-btn {{
            background: #1e293b;
            border: 1px solid #475569;
            color: #fff;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            white-space: nowrap;
            cursor: pointer;
            transition: 0.2s;
        }}
        .filter-btn.active {{
            background: #38bdf8;
            color: #000;
            font-weight: bold;
            border-color: #38bdf8;
        }}

        /* Tombol Shutter / Aksi */
        .action-area {{
            display: flex;
            gap: 10px;
            width: 100%;
            margin-top: 10px;
        }
        .btn {{
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            font-size: 0.85rem;
            cursor: pointer;
            text-align: center;
        }}
        .btn-capture {{
            background: #ffffff;
            color: #000000;
        }}
        .btn-capture:hover {{ background: #e2e8f0; }}
        
        .btn-telegram {{
            background: #0088cc;
            color: #ffffff;
            display: none;
        }}
        .btn-download {{
            background: #22c55e;
            color: #ffffff;
            display: none;
        }}
        .btn-retake {{
            background: #ef4444;
            color: #ffffff;
            display: none;
        }}

        /* Status Notifikasi */
        .status-msg {{
            margin-top: 8px;
            font-size: 0.8rem;
            text-align: center;
            color: #38bdf8;
            min-height: 20px;
        }}
        
        /* Efek Flash Kamera */
        .flash {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: white;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
            z-index: 10;
        }}
        .flash.active {{ opacity: 1; }}
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>✨ VZ LIVE STUDIO</h1>
        <p>Real-Time Camera & Filters</p>
    </div>

    <!-- Kotak Kamera Utama -->
    <div class="camera-box">
        <div id="flashEffect" class="flash"></div>
        <video id="videoElement" autoplay playsinline muted></video>
        <canvas id="canvasElement" style="display: none;"></canvas>
        <img id="photoPreview" style="display: none;" alt="Preview">
    </div>

    <!-- Pilihan Filter Estetik -->
    <div class="filter-selector" id="filterSelector">
        <button class="filter-btn active" onclick="setFilter('filter-normal', this)">Original</button>
        <button class="filter-btn" onclick="setFilter('filter-cyber', this)">Cyber Neon</button>
        <button class="filter-btn" onclick="setFilter('filter-vintage', this)">Vintage Film</button>
        <button class="filter-btn" onclick="setFilter('filter-cinematic', this)">Cinematic</button>
        <button class="filter-btn" onclick="setFilter('filter-mono', this)">Mono Noir</button>
    </div>

    <!-- Input Identitas -->
    <div class="input-group">
        <input type="text" id="usernameInput" placeholder="Ketik nama kamu di sini...">
    </div>

    <!-- Tombol Aksi -->
    <div class="action-area">
        <button id="btnCapture" class="btn btn-capture" onclick="takeSnapshot()">📸 JEPRET</button>
        <button id="btnRetake" class="btn btn-retake" onclick="retakePhoto()">🔄 ULANGI</button>
        <button id="btnDownload" class="btn btn-download" onclick="downloadPhoto()">📥 SIMPAN</button>
        <button id="btnTelegram" class="btn btn-telegram" onclick="sendToTelegram()">🚀 KIRIM TELEGRAM</button>
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
    const btnTelegram = document.getElementById('btnTelegram');
    
    let currentFilter = 'filter-normal';
    let capturedBlob = null;
    let streamInstance = null;

    // Aktifkan Kamera Depan Otomatis
    async function initCamera() {{
        try {{
            streamInstance = await navigator.mediaDevices.getUserMedia({{
                video: {{ facingMode: 'user', width: {{ ideal: 1280 }}, height: {{ ideal: 720 }} }},
                audio: false
            }});
            video.srcObject = streamInstance;
        }} catch (err) {{
            statusText.innerText = "❌ Gagal mengakses kamera. Berikan izin browser!";
        }}
    }}
    initCamera();

    // Ganti Filter Real-Time
    function setFilter(filterClass, btnElement) {{
        currentFilter = filterClass;
        video.className = filterClass;
        
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }}

    // Jepret Foto (Snapshot dari Video Stream)
    function takeSnapshot() {{
        const username = document.getElementById('usernameInput').value.trim();
        if (!username) {{
            statusText.innerText = "⚠️ Harap isi nama kamu terlebih dahulu!";
            return;
        }}
        
        statusText.innerText = "";
        
        // Efek Flash
        flash.classList.add('active');
        setTimeout(() => flash.classList.remove('active'), 300);

        // Render ke Canvas dengan filter yang aktif
        canvas.width = video.videoWidth || 1280;
        canvas.height = video.videoHeight || 720;
        const ctx = canvas.getContext('2d');
        
        // Terapkan filter di canvas agar hasil fotonya sama persis dengan preview
        ctx.filter = window.getComputedStyle(video).filter;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Konversi ke Blob JPEG
        canvas.toBlob((blob) => {{
            capturedBlob = blob;
            const imageUrl = URL.createObjectURL(blob);
            
            preview.src = imageUrl;
            preview.className = currentFilter;
            preview.style.display = 'block';
            video.style.display = 'none';

            // Ubah visibilitas tombol
            btnCapture.style.display = 'none';
            btnRetake.style.display = 'block';
            btnDownload.style.display = 'block';
            btnTelegram.style.display = 'block';
            
            statusText.innerText = "✨ Foto berhasil dijepret!";
        }}, 'image/jpeg', 0.95);
    }}

    // Ulangi Foto
    function retakePhoto() {{
        preview.style.display = 'none';
        video.style.display = 'block';
        
        btnCapture.style.display = 'block';
        btnRetake.style.display = 'none';
        btnDownload.style.display = 'none';
        btnTelegram.style.display = 'none';
        statusText.innerText = "";
    }}

    // Download Foto Lokal
    function downloadPhoto() {{
        if (!capturedBlob) return;
        const username = document.getElementById('usernameInput').value.trim() || 'user';
        const a = document.createElement('a');
        a.href = URL.createObjectURL(capturedBlob);
        a.download = `vz_studio_${username.toLowerCase().replace(/\\s+/g, '_')}.jpg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }}

    // Kirim Langsung ke Telegram via Bot API
    async function sendToTelegram() {{
        if (!capturedBlob) return;
        const username = document.getElementById('usernameInput').value.trim();
        
        btnTelegram.innerText = "Mengirim...";
        btnTelegram.disabled = true;
        
        const botToken = "{TELEGRAM_BOT_TOKEN}";
        const chatId = "{TELEGRAM_CHAT_ID}";
        
        const formData = new FormData();
        formData.append('chat_id', chatId);
        formData.append('photo', capturedBlob, 'selfie.jpg');
        formData.append('caption', `✨ **VZ LIVE STUDIO CAPTURE**\\n\\n👤 Creator: {username}\\n🎨 Filter: ${{currentFilter}}\\n🚀 Status: Berhasil Dikirim Otomatis`);

        try {{
            let response = await fetch(`https://api.telegram.org/bot${{botToken}}/sendPhoto`, {{
                method: 'POST',
                body: formData
            }});
            let result = await response.json();
            
            if (result.ok) {{
                statusText.innerText = "🎉 Foto berhasil terkirim ke Telegram Anda!";
                btnTelegram.innerText = "TERKIRIM ✅";
            }} else {{
                statusText.innerText = "❌ Gagal mengirim: " + (result.description || "Periksa Token Bot");
                btnTelegram.innerText = "🚀 KIRIM TELEGRAM";
                btnTelegram.disabled = false;
            }}
        }} catch (err) {{
            statusText.innerText = "❌ Koneksi error saat mengirim ke Telegram.";
            btnTelegram.innerText = "🚀 KIRIM TELEGRAM";
            btnTelegram.disabled = false;
        }}
    }}
</script>

</body>
</html>
"""

# Render komponen interaktif di Streamlit
components.html(html_code, height=650)
