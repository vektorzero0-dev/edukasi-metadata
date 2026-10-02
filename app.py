import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="VZ Live FX Studio", page_icon="📸", layout="centered"
)

# --- KODE HTML, CSS & JAVASCRIPT (CLEAN UI & MULTI-FX) ---
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VZ Live FX Studio</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        body {
            background: #000000;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            width: 100%;
            padding: 4px;
        }

        .container {
            width: 100%;
            max-width: 440px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .header {
            text-align: center;
            margin-bottom: 4px;
        }
        .header h1 {
            font-size: 1.05rem;
            font-weight: 700;
            color: #f1f5f9;
        }
        .header p {
            font-size: 0.6rem;
            color: #94a3b8;
        }

        /* Kotak Viewfinder Kamera */
        .camera-box {
            position: relative;
            width: 100%;
            aspect-ratio: 4/5;
            background: #111;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 6px 20px rgba(0,0,0,0.8);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        video, canvas, img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            transform: scaleX(-1);
        }
        
        img.captured-preview {
            transform: scaleX(-1);
        }

        /* --- 10 PILIHAN ENGINE / FILTER ESTETIK --- */
        .mode-iphone { filter: brightness(1.08) contrast(1.12) saturate(1.15); }
        .mode-hdr { filter: brightness(1.05) contrast(1.22) saturate(1.20); }
        .mode-portrait { filter: brightness(1.12) contrast(1.08) saturate(1.25) sepia(0.1); }
        .mode-cyber { filter: brightness(1.05) contrast(1.4) saturate(1.8) hue-rotate(310deg); }
        .mode-matrix { filter: brightness(0.95) contrast(1.4) saturate(1.5) hue-rotate(90deg); }
        .mode-cinematic { filter: brightness(1.0) contrast(1.3) saturate(0.9) hue-rotate(-15deg); }
        .mode-vintage { filter: brightness(0.95) contrast(1.1) saturate(0.8) sepia(0.5); }
        .mode-noir { filter: brightness(1.1) contrast(1.6) grayscale(100%); }
        .mode-sunset { filter: brightness(1.05) contrast(1.15) saturate(1.6) sepia(0.2) hue-rotate(-20deg); }
        .mode-raw { filter: none; }

        /* --- EFEK TAMBAHAN (OVERLAYS) --- */
        .fx-vignette::after {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
            pointer-events: none;
            z-index: 5;
        }
        .fx-glow {
            filter: brightness(1.15) contrast(1.05) blur(0.2px) drop-shadow(0 0 8px rgba(255,255,255,0.4)) !important;
        }
        .fx-letterbox::before, .fx-letterbox::after {
            content: '';
            position: absolute;
            left: 0; width: 100%; height: 12%;
            background: #000;
            z-index: 6;
            pointer-events: none;
        }
        .fx-letterbox::before { top: 0; }
        .fx-letterbox::after { bottom: 0; }

        /* Panel Pilihan (Tab Filter & Efek) */
        .control-section {
            width: 100%;
            margin-top: 5px;
        }
        .control-label {
            font-size: 0.58rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 2px;
            font-weight: 700;
        }
        .selector-scroll {
            display: flex;
            gap: 5px;
            width: 100%;
            overflow-x: auto;
            padding: 2px 2px 4px 2px;
            scrollbar-width: none;
        }
        .selector-scroll::-webkit-scrollbar { display: none; }
        
        .opt-btn {
            background: #161b22;
            border: 1px solid #30363d;
            color: #8b949e;
            padding: 5px 9px;
            border-radius: 8px;
            font-size: 0.65rem;
            font-weight: 600;
            white-space: nowrap;
            cursor: pointer;
        }
        .opt-btn.active {
            background: #ffffff;
            color: #000000;
            font-weight: 700;
            border-color: #ffffff;
        }
        .fx-btn.active {
            background: #38bdf8;
            color: #000000;
            border-color: #38bdf8;
        }

        /* Tombol Aksi */
        .action-area {
            display: flex;
            gap: 6px;
            width: 100%;
            margin-top: 6px;
        }
        .btn {
            flex: 1;
            padding: 9px;
            border: none;
            border-radius: 9px;
            font-weight: 700;
            font-size: 0.75rem;
            cursor: pointer;
            text-align: center;
        }
        .btn-capture { background: #ffffff; color: #000000; }
        .btn-retake { background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; display: none; }
        .btn-download { background: rgba(34, 197, 94, 0.2); border: 1px solid rgba(34, 197, 94, 0.4); color: #4ade80; display: none; }

        .status-msg {
            margin-top: 3px;
            font-size: 0.65rem;
            text-align: center;
            color: #38bdf8;
            min-height: 14px;
            font-weight: 500;
        }
        
        .flash {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: white;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.15s ease;
            z-index: 10;
        }
        .flash.active { opacity: 1; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>📸 VZ LIVE FX STUDIO</h1>
        <p>Pro Filters & Live Overlays</p>
    </div>

    <!-- Kotak Kamera dengan kontainer efek -->
    <div class="camera-box" id="cameraBox">
        <div id="flashEffect" class="flash"></div>
        <video id="videoElement" class="mode-iphone" autoplay playsinline muted></video>
        <canvas id="canvasElement" style="display: none;"></canvas>
        <img id="photoPreview" class="captured-preview mode-iphone" style="display: none;" alt="Preview">
    </div>

    <!-- Pilihan Engine Filter (10 Opsi) -->
    <div class="control-section">
        <div class="control-label">Pilih Filter / Warna:</div>
        <div class="selector-scroll" id="filterSelector">
            <button class="opt-btn active" onclick="setFilter('mode-iphone', this)">iPhone HD</button>
            <button class="opt-btn" onclick="setFilter('mode-hdr', this)">Smart HDR</button>
            <button class="opt-btn" onclick="setFilter('mode-portrait', this)">Warm Skin</button>
            <button class="opt-btn" onclick="setFilter('mode-cyber', this)">Cyberpunk</button>
            <button class="opt-btn" onclick="setFilter('mode-matrix', this)">Matrix Green</button>
            <button class="opt-btn" onclick="setFilter('mode-cinematic', this)">Cinematic</button>
            <button class="opt-btn" onclick="setFilter('mode-vintage', this)">Vintage 90s</button>
            <button class="opt-btn" onclick="setFilter('mode-noir', this)">Noir Dark</button>
            <button class="opt-btn" onclick="setFilter('mode-sunset', this)">Golden Hour</button>
            <button class="opt-btn" onclick="setFilter('mode-raw', this)">RAW Original</button>
        </div>
    </div>

    <!-- Pilihan Efek Tambahan -->
    <div class="control-section">
        <div class="control-label">Efek Tambahan (Overlay):</div>
        <div class="selector-scroll" id="fxSelector">
            <button class="opt-btn fx-btn active" onclick="toggleFx('', this)">Normal FX</button>
            <button class="opt-btn fx-btn" onclick="toggleFx('fx-vignette', this)">Vignette Edge</button>
            <button class="opt-btn fx-btn" onclick="toggleFx('fx-glow', this)">Soft Glow</button>
            <button class="opt-btn fx-btn" onclick="toggleFx('fx-letterbox', this)">Cinematic Bars</button>
        </div>
    </div>

    <!-- Tombol Aksi -->
    <div class="action-area">
        <button id="btnCapture" class="btn btn-capture" onclick="takeSnapshot()">📸 JEPRET FOTO</button>
        <button id="btnRetake" class="btn btn-retake" onclick="retakePhoto()">🔄 ULANGI</button>
        <button id="btnDownload" class="btn btn-download" onclick="downloadPhoto()">📥 SIMPAN</button>
    </div>

    <div id="statusText" class="status-msg"></div>
</div>

<script>
    const video = document.getElementById('videoElement');
    const canvas = document.getElementById('canvasElement');
    const preview = document.getElementById('photoPreview');
    const cameraBox = document.getElementById('cameraBox');
    const flash = document.getElementById('flashEffect');
    const statusText = document.getElementById('statusText');
    
    const btnCapture = document.getElementById('btnCapture');
    const btnRetake = document.getElementById('btnRetake');
    const btnDownload = document.getElementById('btnDownload');
    
    let currentFilter = 'mode-iphone';
    let currentFx = '';
    let capturedBlob = null;
    let streamInstance = null;

    async function initCamera() {
        try {
            streamInstance = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } },
                audio: false
            });
            video.srcObject = streamInstance;
        } catch (err) {
            statusText.innerText = "❌ Gagal akses kamera. Berikan izin browser!";
        }
    }
    initCamera();

    function setFilter(filterClass, btnElement) {
        currentFilter = filterClass;
        // Pertahankan efek tambahan di video jika sedang aktif
        video.className = currentFilter + (currentFx ? ' ' + currentFx : '');
        preview.className = "captured-preview " + video.className;
        
        document.querySelectorAll('#filterSelector .opt-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }

    function toggleFx(fxClass, btnElement) {
        currentFx = fxClass;
        video.className = currentFilter + (currentFx ? ' ' + currentFx : '');
        preview.className = "captured-preview " + video.className;
        
        document.querySelectorAll('#fxSelector .opt-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }

    async function takeSnapshot() {
        statusText.innerText = "⚡ Memproses foto HD...";
        
        flash.classList.add('active');
        setTimeout(() => flash.classList.remove('active'), 200);

        canvas.width = video.videoWidth || 1280;
        canvas.height = video.videoHeight || 720;
        const ctx = canvas.getContext('2d');
        
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        ctx.filter = window.getComputedStyle(video).filter;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            capturedBlob = blob;
            preview.src = URL.createObjectURL(blob);
            preview.style.display = 'block';
            video.style.display = 'none';

            btnCapture.style.display = 'none';
            btnRetake.style.display = 'block';
            btnDownload.style.display = 'block';
            statusText.innerText = "🎉 Foto berhasil dijepret! Silakan unduh.";
        }, 'image/jpeg', 0.95);
    }

    function retakePhoto() {
        preview.style.display = 'none';
        video.style.display = 'block';
        btnCapture.style.display = 'block';
        btnRetake.style.display = 'none';
        btnDownload.style.display = 'none';
        statusText.innerText = "";
    }

    function downloadPhoto() {
        if (!capturedBlob) return;
        const a = document.createElement('a');
        a.href = URL.createObjectURL(capturedBlob);
        a.download = `vz_studio_${Date.now()}.jpg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
</script>

</body>
</html>
"""

# Render komponen dengan tinggi iframe 750px agar semua tombol filter & efek tampil sempurna
components.html(html_code, height=750)
