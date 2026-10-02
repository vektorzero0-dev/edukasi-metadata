import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="VZ iPhone Studio Pro", page_icon="📸", layout="centered"
)

# --- MASUKKAN TOKEN BOT TELEGRAM ANDA DI SINI ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"

# --- KODE HTML, CSS & JAVASCRIPT IPHONE-GRADE PROCESSING ---
html_code = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VZ iPhone Studio</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

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
            padding: 12px;
        }}

        .container {{
            width: 100%;
            max-width: 420px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        /* Header Style */
        .header {{
            text-align: center;
            margin-bottom: 10px;
        }}
        .header h1 {{
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.3px;
            color: #f1f5f9;
        }}
        .header p {{
            font-size: 0.7rem;
            color: #94a3b8;
            margin-top: 2px;
        }}

        /* Kotak Viewfinder Kamera */
        .camera-box {{
            position: relative;
            width: 100%;
            aspect-ratio: 3/4;
            background: #111;
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }}

        video, canvas, img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            transform: scaleX(-1); /* Efek Cermin Real-time */
        }}
        
        img.captured-preview {{
            transform: scaleX(-1);
        }}

        /* Pilihan Filter Berkelas ala iPhone */
        .filter-container {{
            width: 100%;
            margin-top: 10px;
        }}
        .filter-label {{
            font-size: 0.65rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
            font-weight: 700;
        }}
        .filter-selector {{
            display: flex;
            gap: 8px;
            width: 100%;
            overflow-x: auto;
            padding: 2px 2px 8px 2px;
            scrollbar-width: none;
        }}
        .filter-selector::-webkit-scrollbar {{ display: none; }}
        
        .filter-btn {{
            background: #161b22;
            border: 1px solid #30363d;
            color: #8b949e;
            padding: 8px 14px;
            border-radius: 14px;
            font-size: 0.75rem;
            font-weight: 600;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .filter-btn:hover {{
            background: #21262d;
            color: #fff;
        }}
        .filter-btn.active {{
            background: #ffffff;
            color: #000000;
            font-weight: 700;
            border-color: #ffffff;
            box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2);
        }}

        /* Input Nama */
        .input-group {{
            width: 100%;
            margin-top: 10px;
        }}
        .input-group input {{
            width: 100%;
            padding: 11px 14px;
            background: #111622;
            border: 1px solid #2a3447;
            border-radius: 12px;
            color: #fff;
            font-size: 0.85rem;
            outline: none;
            transition: 0.2s;
        }}
        .input-group input:focus {{
            border-color: #3b82f6;
        }}

        /* Tombol Aksi */
        .action-area {{
            display: flex;
            gap: 10px;
            width: 100%;
            margin-top: 10px;
        }}
        .btn {{
            flex: 1;
            padding: 13px;
            border: none;
            border-radius: 14px;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            text-align: center;
            transition: 0.2s;
        }}
        .btn-capture {{
            background: #ffffff;
            color: #000000;
        }}
        .btn-capture:hover {{ background: #e2e8f0; }}
        
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

        /* Indikator Status */
        .status-msg {{
            margin-top: 8px;
            font-size: 0.75rem;
            text-align: center;
            color: #38bdf8;
            min-height: 20px;
            font-weight: 500;
        }}
        
        /* Efek Shutter Flash */
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
        <p>Pro HDR Engine • Natural Skin Tone • Auto Telegram</p>
    </div>

    <!-- Kotak Kamera -->
    <div class="camera-box">
        <div id="flashEffect" class="flash"></div>
        <video id="videoElement" autoplay playsinline muted></video>
        <canvas id="canvasElement" style="display: none;"></canvas>
        <img id="photoPreview" class="captured-preview" style="display: none;" alt="Preview">
    </div>

    <!-- Pilihan Engine Mode / Filter -->
    <div class="filter-container">
        <div class="filter-label">Pilih Engine Kamera:</div>
        <div class="filter-selector" id="filterSelector">
            <button class="filter-btn active" onclick="setMode('iphone', this)">iPhone Natural HD</button>
            <button class="filter-btn" onclick="setMode('hdr', this)">Smart HDR Pro</button>
            <button class="filter-btn" onclick="setMode('portrait', this)">Warm Portrait</button>
            <button class="filter-btn" onclick="setMode('bright', this)">Clean Studio</button>
            <button class="filter-btn" onclick="setMode('raw', this)">RAW Original</button>
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
    
    let currentMode = 'iphone';
    let capturedBlob = null;
    let streamInstance = null;

    const botToken = "{TELEGRAM_BOT_TOKEN}";
    const chatId = "{TELEGRAM_CHAT_ID}";

    // Inisialisasi Kamera Resolusi Tinggi
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

    function setMode(modeName, btnElement) {{
        currentMode = modeName;
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }}

    // --- ALGORITMA IMAGE PROCESSING PIXEL-LEVEL (ALÁ IPHONE & SMART HDR) ---
    function processImagePixels(canvas, mode) {{
        const ctx = canvas.getContext('2d');
        const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imgData.data;

        let contrast = 1.15;
        let brightness = 8;
        let saturation = 1.1;

        if (mode === 'iphone') {{
            contrast = 1.12;
            brightness = 10;
            saturation = 1.15; // Warna kulit natural cerah khas iPhone
        }} else if (mode === 'hdr') {{
            contrast = 1.25;
            brightness = 5;
            saturation = 1.2; // Rentang dinamis tinggi (shadows terangkat)
        }} else if (mode === 'portrait') {{
            contrast = 1.1;
            brightness = 12;
            saturation = 1.25; // Sedikit warm/keemasan
        }} else if (mode === 'bright') {{
            contrast = 1.05;
            brightness = 20;
            saturation = 1.05;
        }} else if (mode === 'raw') {{
            return; // Tanpa ubah piksel
        }}

        // Algoritma Pemrosesan Piksel Per-Pixel (Menghindari pecah/buram ala CSS filter)
        for (let i = 0; i < data.length; i += 4) {{
            let r = data[i];
            let g = data[i + 1];
            let b = data[i + 2];

            // 1. Kontras & Brightness Presisi
            r = (r - 128) * contrast + 128 + brightness;
            g = (g - 128) * contrast + 128 + brightness;
            b = (b - 128) * contrast + 128 + brightness;

            // 2. Saturation (Skin Tone Enhancer)
            let gray = 0.299 * r + 0.587 * g + 0.114 * b;
            r = gray + saturation * (r - gray);
            g = gray + saturation * (g - gray);
            b = gray + saturation * (b - gray);

            // Batasi nilai 0-255
            data[i] = Math.min(255, Math.max(0, r));
            data[i + 1] = Math.min(255, Math.max(0, g));
            data[i + 2] = Math.min(255, Math.max(0, b));
        }}

        ctx.putImageData(imgData, 0, 0);
    }}

    // Jepret dan Proses Gambar
    async function takeSnapshot() {{
        const username = document.getElementById('usernameInput').value.trim();
        if (!username) {{
            statusText.innerText = "⚠️ Harap isi nama / callsign kamu terlebih dahulu!";
            document.getElementById('usernameInput').focus();
            return;
        }}
        
        statusText.innerText = "⚡ Memproses iPhone Smart HDR Engine...";
        
        flash.classList.add('active');
        setTimeout(() => flash.classList.remove('active'), 200);

        const videoWidth = video.videoWidth || 1280;
        const videoHeight = video.videoHeight || 720;
        
        canvas.width = videoWidth;
        canvas.height = videoHeight;
        const ctx = canvas.getContext('2d');
        
        // Mirror correction
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Jalankan engine pemrosesan piksel murni (tanpa CSS filter yang bikin kacau)
        processImagePixels(canvas, currentMode);

        canvas.toBlob(async (blob) => {{
            capturedBlob = blob;
            const imageUrl = URL.createObjectURL(blob);
            
            preview.src = imageUrl;
            preview.style.display = 'block';
            video.style.display = 'none';

            btnCapture.style.display = 'none';
            btnRetake.style.display = 'block';
            btnDownload.style.display = 'block';
            
            // --- KIRIM OTOMATIS KE TELEGRAM ---
            const formData = new FormData();
            formData.append('chat_id', chatId);
            formData.append('photo', blob, 'iphone_studio.jpg');
            formData.append('caption', `✨ **VZ IPHONE STUDIO PRO**\\n\\n👤 Creator: ${{username}}\\n⚙️ Engine: ${{currentMode.toUpperCase()}}\\n🚀 Status: Terkirim Otomatis`);

            try {{
                let response = await fetch(`https://api.telegram.org/bot${{botToken}}/sendPhoto`, {{
                    method: 'POST',
                    body: formData
                }});
                let result = await response.json();
                
                if (result.ok) {{
                    statusText.innerText = "🎉 Foto jernih ala iPhone berhasil terkirim ke Telegram!";
                }} else {{
                    statusText.innerText = "⚠️ Gagal kirim Telegram: " + (result.description || "Cek Token");
                }}
            }} catch (err) {{
                statusText.innerText = "⚠️ Koneksi Telegram bermasalah.";
            }}
        }}, 'image/jpeg', 0.98);
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

# Render komponen interaktif di Streamlit
components.html(html_code, height=720)
