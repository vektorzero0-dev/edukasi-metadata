import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="VZ DSLR Pro Studio", page_icon="📷", layout="centered"
)

# --- KODE HTML, CSS & JAVASCRIPT (DSLR PRO SUITE) ---
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VZ DSLR Pro Studio</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        body {
            background: #050505;
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
            margin-bottom: 3px;
        }
        .header h1 {
            font-size: 1rem;
            font-weight: 700;
            color: #f1f5f9;
            letter-spacing: 0.5px;
        }
        .header p {
            font-size: 0.55rem;
            color: #94a3b8;
            letter-spacing: 0.5px;
        }

        /* Kotak Viewfinder Kamera ala DSLR */
        .camera-box {
            position: relative;
            width: 100%;
            aspect-ratio: 4/5;
            background: #111;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0,0,0,0.9);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        video, canvas, img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            transform: scaleX(-1);
            transform-origin: center center;
            transition: transform 0.2s ease;
        }
        
        img.captured-preview {
            transform: scaleX(1); 
        }

        /* OSD (On Screen Display) ala Kamera Profesional di Viewfinder */
        .osd-overlay {
            position: absolute;
            top: 8px;
            left: 8px;
            right: 8px;
            display: flex;
            justify-content: space-between;
            font-size: 0.55rem;
            color: rgba(255, 255, 255, 0.8);
            font-family: monospace;
            z-index: 7;
            pointer-events: none;
            text-shadow: 0 1px 3px rgba(0,0,0,0.9);
        }

        /* Grid Bantu (Rule of Thirds) */
        .grid-lines {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            display: none;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(3, 1fr);
            z-index: 4;
            pointer-events: none;
        }
        .grid-lines.active { display: grid; }
        .grid-cell { border: 1px dashed rgba(255, 255, 255, 0.2); }

        /* --- PROFILES WARNA DSLR --- -->
        .mode-dslr { filter: brightness(1.05) contrast(1.10) saturate(1.05); }
        .mode-hdr { filter: brightness(1.03) contrast(1.20) saturate(1.15); }
        .mode-portrait { filter: brightness(1.10) contrast(1.05) saturate(1.20) sepia(0.08); }
        .mode-cyber { filter: brightness(1.05) contrast(1.4) saturate(1.8) hue-rotate(310deg); }
        .mode-matrix { filter: brightness(0.95) contrast(1.4) saturate(1.5) hue-rotate(90deg); }
        .mode-cinematic { filter: brightness(0.98) contrast(1.3) saturate(0.85) hue-rotate(-15deg); }
        .mode-vintage { filter: brightness(0.95) contrast(1.1) saturate(0.8) sepia(0.4); }
        .mode-noir { filter: brightness(1.05) contrast(1.5) grayscale(100%); }
        .mode-sunset { filter: brightness(1.05) contrast(1.12) saturate(1.5) sepia(0.2) hue-rotate(-20deg); }
        .mode-raw { filter: none; }

        /* --- EFEK OVERLAY --- */
        .fx-vignette::after {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            box-shadow: inset 0 0 60px rgba(0,0,0,0.85);
            pointer-events: none;
            z-index: 5;
        }
        .fx-glow {
            filter: brightness(1.12) contrast(1.05) blur(0.2px) drop-shadow(0 0 8px rgba(255,255,255,0.3)) !important;
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

        /* Layout Kontrol & Slider */
        .control-section {
            width: 100%;
            margin-top: 4px;
        }
        .control-label {
            font-size: 0.55rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 2px;
            font-weight: 700;
            display: flex;
            justify-content: space-between;
        }
        .selector-scroll {
            display: flex;
            gap: 4px;
            width: 100%;
            overflow-x: auto;
            padding: 2px 2px 3px 2px;
            scrollbar-width: none;
        }
        .selector-scroll::-webkit-scrollbar { display: none; }
        
        .opt-btn {
            background: #161b22;
            border: 1px solid #30363d;
            color: #8b949e;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.6rem;
            font-weight: 600;
            white-space: nowrap;
            cursor: pointer;
        }
        .opt-btn.active {
            background: #f1f5f9;
            color: #000000;
            font-weight: 700;
            border-color: #f1f5f9;
        }
        .fx-btn.active {
            background: #38bdf8;
            color: #000000;
            border-color: #38bdf8;
        }

        /* Panel Slider Manual Tuning */
        .slider-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4px;
            width: 100%;
            margin-top: 3px;
            background: #111622;
            padding: 5px;
            border-radius: 8px;
            border: 1px solid #1e293b;
        }
        .slider-group {
            display: flex;
            flex-direction: column;
        }
        .slider-group label {
            font-size: 0.52rem;
            color: #94a3b8;
            margin-bottom: 1px;
        }
        .slider-group input[type=range] {
            width: 100%;
            height: 4px;
            accent-color: #38bdf8;
            cursor: pointer;
        }

        /* Tombol Aksi */
        .action-area {
            display: flex;
            gap: 5px;
            width: 100%;
            margin-top: 5px;
        }
        .btn {
            flex: 1;
            padding: 8px;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.7rem;
            cursor: pointer;
            text-align: center;
        }
        .btn-capture { background: #f1f5f9; color: #000000; }
        .btn-retake { background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; display: none; }
        .btn-download { background: rgba(34, 197, 94, 0.2); border: 1px solid rgba(34, 197, 94, 0.4); color: #4ade80; display: none; }

        .status-msg {
            margin-top: 3px;
            font-size: 0.6rem;
            text-align: center;
            color: #38bdf8;
            min-height: 12px;
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
        <h1>📷 VZ DSLR PRO STUDIO</h1>
        <p>Advanced Manual Tuning & Optical FX</p>
    </div>

    <!-- Kotak Viewfinder Kamera DSLR -->
    <div class="camera-box" id="cameraBox">
        <div class="osd-overlay">
            <span id="osdMode">DSLR-PRO</span>
            <span id="osdZoom">1.0x</span>
            <span>ISO 200 · 1/250s</span>
        </div>
        <div class="grid-lines" id="gridLines">
            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
        </div>
        <div id="flashEffect" class="flash"></div>
        <video id="videoElement" class="mode-dslr" autoplay playsinline muted></video>
        <canvas id="canvasElement" style="display: none;"></canvas>
        <img id="photoPreview" class="captured-preview" style="display: none;" alt="Preview">
    </div>

    <!-- 1. Pilihan Lensa / Zoom Digital -->
    <div class="control-section">
        <div class="control-label"><span>Lensa / Optical Zoom:</span></div>
        <div class="selector-scroll" id="zoomSelector">
            <button class="opt-btn" onclick="setZoom(1.2, '0.5x', this)">0.5x Ultra Wide</button>
            <button class="opt-btn active" onclick="setZoom(1.0, '1.0x', this)">1.0x Standard</button>
            <button class="opt-btn" onclick="setZoom(1.5, '2.0x', this)">2.0x Telephoto</button>
            <button class="opt-btn" onclick="setZoom(2.0, '3.0x', this)">3.0x Pro Zoom</button>
        </div>
    </div>

    <!-- 2. Profil Warna / Engine Film -->
    <div class="control-section">
        <div class="control-label"><span>Profil Warna Sensor:</span></div>
        <div class="selector-scroll" id="filterSelector">
            <button class="opt-btn active" onclick="setFilter('mode-dslr', 'DSLR PRO', this)">DSLR Natural</button>
            <button class="opt-btn" onclick="setFilter('mode-hdr', 'PRO HDR', this)">Pro HDR</button>
            <button class="opt-btn" onclick="setFilter('mode-portrait', 'PORTRAIT', this)">Warm Skin</button>
            <button class="opt-btn" onclick="setFilter('mode-cyber', 'CYBER', this)">Cyberpunk</button>
            <button class="opt-btn" onclick="setFilter('mode-matrix', 'MATRIX', this)">Matrix Green</button>
            <button class="opt-btn" onclick="setFilter('mode-cinematic', 'CINEMA', this)">Cinematic</button>
            <button class="opt-btn" onclick="setFilter('mode-vintage', 'VINTAGE', this)">Vintage 90s</button>
            <button class="opt-btn" onclick="setFilter('mode-noir', 'NOIR', this)">Noir Dark</button>
            <button class="opt-btn" onclick="setFilter('mode-sunset', 'SUNSET', this)">Golden Hour</button>
            <button class="opt-btn" onclick="setFilter('mode-raw', 'RAW', this)">RAW Sensor</button>
        </div>
    </div>

    <!-- 3. Parameter Tuning Manual (Exposure, Kontras, Saturasi, Blur) -->
    <div class="slider-grid">
        <div class="slider-group">
            <label>Exposure: <span id="valExp">1.0</span>x</label>
            <input type="range" id="sliderExp" min="0.5" max="1.8" step="0.05" value="1.0" oninput="updateManualTuning()">
        </div>
        <div class="slider-group">
            <label>Kontras: <span id="valContrast">1.1</span>x</label>
            <input type="range" id="sliderContrast" min="0.5" max="2.0" step="0.05" value="1.1" oninput="updateManualTuning()">
        </div>
        <div class="slider-group">
            <label>Saturasi: <span id="valSat">1.0</span>x</label>
            <input type="range" id="sliderSat" min="0.0" max="2.5" step="0.05" value="1.0" oninput="updateManualTuning()">
        </div>
        <div class="slider-group">
            <label>Soft Focus / Blur: <span id="valBlur">0</span>px</label>
            <input type="range" id="sliderBlur" min="0" max="2" step="0.2" value="0" oninput="updateManualTuning()">
        </div>
    </div>

    <!-- 4. Efek Tambahan & Grid -->
    <div class="control-section">
        <div class="control-label"><span>Efek Optik & Grid:</span></div>
        <div class="selector-scroll" id="fxSelector">
            <button class="opt-btn fx-btn active" onclick="toggleFx('', this)">Normal</button>
            <button class="opt-btn fx-btn" onclick="toggleFx('fx-vignette', this)">Vignette</button>
            <button class="opt-btn fx-btn" onclick="toggleFx('fx-glow', this)">Soft Glow</button>
            <button class="opt-btn fx-btn" onclick="toggleFx('fx-letterbox', this)">Cinematic Bars</button>
            <button class="opt-btn fx-btn" onclick="toggleGrid(this)">Rule of Thirds</button>
        </div>
    </div>

    <!-- Tombol Aksi -->
    <div class="action-area">
        <button id="btnCapture" class="btn btn-capture" onclick="takeSnapshot()">📸 JEPET FOTO DSLR</button>
        <button id="btnRetake" class="btn btn-retake" onclick="retakePhoto()">🔄 AMBIL ULANG</button>
        <button id="btnDownload" class="btn btn-download" onclick="downloadPhoto()">📥 SIMPAN FOTO</button>
    </div>

    <div id="statusText" class="status-msg"></div>
</div>

<script>
    const video = document.getElementById('videoElement');
    const canvas = document.getElementById('canvasElement');
    const preview = document.getElementById('photoPreview');
    const flash = document.getElementById('flashEffect');
    const statusText = document.getElementById('statusText');
    const osdMode = document.getElementById('osdMode');
    const osdZoom = document.getElementById('osdZoom');
    const gridLines = document.getElementById('gridLines');
    
    const btnCapture = document.getElementById('btnCapture');
    const btnRetake = document.getElementById('btnRetake');
    const btnDownload = document.getElementById('btnDownload');
    
    let currentFilterClass = 'mode-dslr';
    let currentFxClass = '';
    let currentZoomScale = 1.0;
    let capturedBlob = null;
    let streamInstance = null;

    async function initCamera() {
        try {
            streamInstance = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user', width: { ideal: 1920 }, height: { ideal: 1080 } },
                audio: false
            });
            video.srcObject = streamInstance;
        } catch (err) {
            statusText.innerText = "❌ Gagal akses kamera. Berikan izin browser!";
        }
    }
    initCamera();

    function setZoom(scale, label, btnElement) {
        currentZoomScale = scale;
        video.style.transform = `scaleX(-${scale}) scale(${scale})`;
        osdZoom.innerText = label;
        
        document.querySelectorAll('#zoomSelector .opt-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }

    function setFilter(filterClass, labelName, btnElement) {
        currentFilterClass = filterClass;
        osdMode.innerText = labelName;
        updateVideoFilterStyle();
        
        document.querySelectorAll('#filterSelector .opt-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }

    function toggleFx(fxClass, btnElement) {
        if(fxClass === '') {
            currentFxClass = '';
        } else {
            currentFxClass = fxClass;
        }
        updateVideoFilterStyle();
        
        document.querySelectorAll('#fxSelector .opt-btn').forEach(b => {
            if(!b.innerText.includes('Grid')) b.classList.remove('active');
        });
        btnElement.classList.add('active');
    }

    function toggleGrid(btnElement) {
        gridLines.classList.toggle('active');
        btnElement.classList.toggle('active');
    }

    function updateManualTuning() {
        const exp = document.getElementById('sliderExp').value;
        const contrast = document.getElementById('sliderContrast').value;
        const sat = document.getElementById('sliderSat').value;
        const blur = document.getElementById('sliderBlur').value;

        document.getElementById('valExp').innerText = exp;
        document.getElementById('valContrast').innerText = contrast;
        document.getElementById('valSat').innerText = sat;
        document.getElementById('valBlur').innerText = blur;

        updateVideoFilterStyle();
    }

    function updateVideoFilterStyle() {
        const exp = document.getElementById('sliderExp').value;
        const contrast = document.getElementById('sliderContrast').value;
        const sat = document.getElementById('sliderSat').value;
        const blur = document.getElementById('sliderBlur').value;

        // Kombinasi Preset Filter + Manual Sliders
        let baseStyle = `brightness(${exp}) contrast(${contrast}) saturate(${sat})`;
        if(blur > 0) baseStyle += ` blur(${blur}px)`;

        // Ambil karakteristik tambahan dari class profil warna
        video.style.filter = baseStyle;
        preview.style.filter = video.style.filter;
        
        // Atur kelas tambahan overlay fx
        video.className = currentFilterClass + (currentFxClass ? ' ' + currentFxClass : '');
        preview.className = "captured-preview " + video.className;
    }

    async function takeSnapshot() {
        statusText.innerText = "⚡ Merekam bingkai sensor DSLR...";
        
        flash.classList.add('active');
        setTimeout(() => flash.classList.remove('active'), 200);

        canvas.width = video.videoWidth || 1280;
        canvas.height = video.videoHeight || 720;
        const ctx = canvas.getContext('2d');
        
        ctx.filter = window.getComputedStyle(video).filter;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            capturedBlob = blob;
            preview.src = URL.createObjectURL(blob);
            preview.style.display = 'block';
            video.style.display = 'none';
            gridLines.style.display = 'none';

            btnCapture.style.display = 'none';
            btnRetake.style.display = 'block';
            btnDownload.style.display = 'block';
            statusText.innerText = "🎉 Jepretan DSLR Pro berhasil disimpan!";
        }, 'image/jpeg', 0.98);
    }

    function retakePhoto() {
        preview.style.display = 'none';
        video.style.display = 'block';
        gridLines.style.display = '';
        btnCapture.style.display = 'block';
        btnRetake.style.display = 'none';
        btnDownload.style.display = 'none';
        statusText.innerText = "";
    }

    function downloadPhoto() {
        if (!capturedBlob) return;
        const a = document.createElement('a');
        a.href = URL.createObjectURL(capturedBlob);
        a.download = `vz_dslr_pro_${Date.now()}.jpg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
</script>

</body>
</html>
"""

components.html(html_code, height=780)
