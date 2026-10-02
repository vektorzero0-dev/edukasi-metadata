import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="VZ DSLR Telegram Pro Ultimate", page_icon="📷", layout="centered"
)

# --- MASUKKAN TOKEN BOT & CHAT ID TELEGRAM ANDA DI SINI ---
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"

# --- MENGGUNAKAN RAW STRING (r""") ATAU MENGHAPUS 'f' JIKA TIDAK ADA VARIABEL PYTHON DI DALAM HTML ---
# Catatan: Karena token dan chat_id disuntikkan secara aman via string formatting terpisah,
# kita ubah f-string menjadi string biasa (tanpa awalan f) agar tidak bentrok dengan kurung kurawal CSS/JS.
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VZ DSLR Telegram Pro Ultimate</title>
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
            padding: 2px;
        }

        .container {
            width: 100%;
            max-width: 420px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .header {
            text-align: center;
            margin-bottom: 2px;
        }
        .header h1 {
            font-size: 0.95rem;
            font-weight: 700;
            color: #f1f5f9;
        }
        .header p {
            font-size: 0.5rem;
            color: #38bdf8;
        }

        /* Kotak Viewfinder Kamera DSLR */
        .camera-box {
            position: relative;
            width: 100%;
            aspect-ratio: 4/5;
            background: #111;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.8);
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
        }
        
        img.captured-preview {
            transform: scaleX(1); 
        }

        /* OSD (On Screen Display) */
        .osd-overlay {
            position: absolute;
            top: 6px;
            left: 6px;
            right: 6px;
            display: flex;
            justify-content: space-between;
            font-size: 0.5rem;
            color: rgba(255, 255, 255, 0.85);
            font-family: monospace;
            z-index: 7;
            pointer-events: none;
            text-shadow: 0 1px 2px rgba(0,0,0,0.9);
        }

        /* Countdown Overlay */
        .countdown-overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            font-weight: 700;
            color: #38bdf8;
            background: rgba(0,0,0,0.4);
            z-index: 9;
            display: none;
            text-shadow: 0 2px 10px rgba(0,0,0,0.8);
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

        /* --- EFEK OVERLAY CSS --- */
        .fx-vignette::after {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.9);
            pointer-events: none;
            z-index: 5;
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

        /* Panel Kontrol */
        .control-section {
            width: 100%;
            margin-top: 3px;
        }
        .control-label {
            font-size: 0.52rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 1px;
            font-weight: 700;
            display: flex;
            justify-content: space-between;
        }
        .selector-scroll {
            display: flex;
            gap: 3px;
            width: 100%;
            overflow-x: auto;
            padding: 1px 1px 2px 1px;
            scrollbar-width: none;
        }
        .selector-scroll::-webkit-scrollbar { display: none; }
        
        .opt-btn {
            background: #161b22;
            border: 1px solid #30363d;
            color: #8b949e;
            padding: 3px 7px;
            border-radius: 5px;
            font-size: 0.58rem;
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

        /* Panel Konfigurasi Watermark & Slider */
        .config-panel {
            display: flex;
            gap: 3px;
            width: 100%;
            margin-top: 3px;
        }
        .input-group {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .input-group label {
            font-size: 0.5rem;
            color: #8b949e;
            margin-bottom: 1px;
        }
        .input-group input {
            background: #0d1117;
            border: 1px solid #30363d;
            color: #fff;
            padding: 4px;
            border-radius: 5px;
            font-size: 0.6rem;
            outline: none;
        }

        /* Panel Slider Manual Tuning */
        .slider-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3px;
            width: 100%;
            margin-top: 3px;
            background: #0d1117;
            padding: 4px;
            border-radius: 6px;
            border: 1px solid #21262d;
        }
        .slider-group {
            display: flex;
            flex-direction: column;
        }
        .slider-group label {
            font-size: 0.5rem;
            color: #8b949e;
            margin-bottom: 1px;
        }
        .slider-group input[type=range] {
            width: 100%;
            height: 3px;
            accent-color: #38bdf8;
            cursor: pointer;
        }

        /* Tombol Aksi */
        .action-area {
            display: flex;
            gap: 4px;
            width: 100%;
            margin-top: 4px;
        }
        .btn {
            flex: 1;
            padding: 7px;
            border: none;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.65rem;
            cursor: pointer;
            text-align: center;
        }
        .btn-capture { background: #f1f5f9; color: #000000; }
        .btn-retake { background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; display: none; }
        .btn-download { background: rgba(34, 197, 94, 0.2); border: 1px solid rgba(34, 197, 94, 0.4); color: #4ade80; display: none; }

        .status-msg {
            margin-top: 2px;
            font-size: 0.55rem;
            text-align: center;
            color: #38bdf8;
            min-height: 10px;
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
        <h1>📷 VZ DSLR TELEGRAM PRO ULTIMATE</h1>
        <p>Pro Tuning, Watermark & Auto Telegram Sender</p>
    </div>

    <!-- Kotak Viewfinder Kamera DSLR -->
    <div class="camera-box" id="cameraBox">
        <div class="osd-overlay">
            <span id="osdMode">DSLR-PRO</span>
            <span id="osdZoom">1.0x</span>
            <span>ISO 200 · 1/250s</span>
        </div>
        <div class="countdown-overlay" id="countdownOverlay">3</div>
        <div class="grid-lines" id="gridLines">
            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
        </div>
        <div id="flashEffect" class="flash"></div>
        <video id="videoElement" autoplay playsinline muted></video>
        <canvas id="canvasElement" style="display: none;"></canvas>
        <img id="photoPreview" class="captured-preview" style="display: none;" alt="Preview">
    </div>

    <!-- Watermark & Timer Config -->
    <div class="config-panel">
        <div class="input-group">
            <label>Teks Watermark Foto:</label>
            <input type="text" id="watermarkText" value="VEKTOR ZERO CYBER | VZ ZEEO">
        </div>
        <div class="input-group" style="max-width: 110px;">
            <label>Timer Shutter:</label>
            <div class="selector-scroll" style="gap:2px;">
                <button class="opt-btn active" onclick="setTimer(0, this)">0s</button>
                <button class="opt-btn" onclick="setTimer(3, this)">3s</button>
                <button class="opt-btn" onclick="setTimer(5, this)">5s</button>
            </div>
        </div>
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
            <button class="opt-btn active" onclick="setPreset('dslr', 'DSLR PRO', this)">DSLR Natural</button>
            <button class="opt-btn" onclick="setPreset('hdr', 'PRO HDR', this)">Pro HDR</button>
            <button class="opt-btn" onclick="setPreset('portrait', 'PORTRAIT', this)">Warm Skin</button>
            <button class="opt-btn" onclick="setPreset('cyber', 'CYBER', this)">Cyberpunk</button>
            <button class="opt-btn" onclick="setPreset('matrix', 'MATRIX', this)">Matrix Green</button>
            <button class="opt-btn" onclick="setPreset('cinematic', 'CINEMA', this)">Cinematic</button>
            <button class="opt-btn" onclick="setPreset('vintage', 'VINTAGE', this)">Vintage 90s</button>
            <button class="opt-btn" onclick="setPreset('noir', 'NOIR', this)">Noir Dark</button>
            <button class="opt-btn" onclick="setPreset('sunset', 'SUNSET', this)">Golden Hour</button>
            <button class="opt-btn" onclick="setPreset('raw', 'RAW', this)">RAW Sensor</button>
        </div>
    </div>

    <!-- 3. Parameter Tuning Manual -->
    <div class="slider-grid">
        <div class="slider-group">
            <label>Exposure: <span id="valExp">1.0</span>x</label>
            <input type="range" id="sliderExp" min="0.5" max="1.8" step="0.05" value="1.0" oninput="updateFilters()">
        </div>
        <div class="slider-group">
            <label>Kontras: <span id="valContrast">1.1</span>x</label>
            <input type="range" id="sliderContrast" min="0.5" max="2.0" step="0.05" value="1.1" oninput="updateFilters()">
        </div>
        <div class="slider-group">
            <label>Saturasi: <span id="valSat">1.0</span>x</label>
            <input type="range" id="sliderSat" min="0.0" max="2.5" step="0.05" value="1.0" oninput="updateFilters()">
        </div>
        <div class="slider-group">
            <label>Soft Focus / Blur: <span id="valBlur">0</span>px</label>
            <input type="range" id="sliderBlur" min="0" max="2" step="0.2" value="0" oninput="updateFilters()">
        </div>
    </div>

    <!-- 4. Efek Optik & Grid -->
    <div class="control-section">
        <div class="control-label"><span>Efek Optik & Grid:</span></div>
        <div class="selector-scroll" id="fxSelector">
            <button class="opt-btn fx-btn active" onclick="toggleFx('', this)">Normal</button>
            <button class="opt-btn fx-btn" onclick="toggleFx('fx-vignette', this)">Vignette</button>
            <button class="opt-btn fx-btn" onclick="toggleFx('fx-letterbox', this)">Cinematic Bars</button>
            <button class="opt-btn fx-btn" onclick="toggleGrid(this)">Rule of Thirds</button>
        </div>
    </div>

    <!-- Tombol Aksi -->
    <div class="action-area">
        <button id="btnCapture" class="btn btn-capture" onclick="startCaptureProcess()">📸 JEPRET & KIRIM TELEGRAM</button>
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
    const countdownOverlay = document.getElementById('countdownOverlay');
    
    const btnCapture = document.getElementById('btnCapture');
    const btnRetake = document.getElementById('btnRetake');
    const btnDownload = document.getElementById('btnDownload');
    
    let currentPreset = 'dslr';
    let currentFx = '';
    let currentZoomScale = 1.0;
    let selectedTimer = 0;
    let capturedBlob = null;

    // Token & Chat ID disuntikkan secara aman via string replacement di Python
    const botToken = "REPLACE_BOT_TOKEN";
    const chatId = "REPLACE_CHAT_ID";

    async function initCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } },
                audio: false
            });
            video.srcObject = stream;
        } catch (err) {
            statusText.innerText = "❌ Gagal akses kamera. Berikan izin browser!";
        }
    }
    initCamera();

    function setTimer(seconds, btnElement) {
        selectedTimer = seconds;
        document.querySelectorAll('.config-panel .opt-btn').forEach(b => {
            b.classList.remove('active');
        });
        btnElement.classList.add('active');
    }

    function setZoom(scale, label, btnElement) {
        currentZoomScale = scale;
        video.style.transform = `scaleX(-${scale}) scale(${scale})`;
        preview.style.transform = `scale(${scale})`;
        osdZoom.innerText = label;
        
        document.querySelectorAll('#zoomSelector .opt-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }

    function setPreset(presetName, labelName, btnElement) {
        currentPreset = presetName;
        osdMode.innerText = labelName;
        updateFilters();
        
        document.querySelectorAll('#filterSelector .opt-btn').forEach(b => b.classList.remove('active'));
        btnElement.classList.add('active');
    }

    function toggleFx(fxClass, btnElement) {
        currentFx = fxClass;
        const cameraBox = document.getElementById('cameraBox');
        cameraBox.className = "camera-box " + currentFx;
        
        document.querySelectorAll('#fxSelector .opt-btn').forEach(b => {
            if(!b.innerText.includes('Grid')) b.classList.remove('active');
        });
        btnElement.classList.add('active');
    }

    function toggleGrid(btnElement) {
        gridLines.classList.toggle('active');
        btnElement.classList.toggle('active');
    }

    function updateFilters() {
        const exp = parseFloat(document.getElementById('sliderExp').value);
        const contrast = parseFloat(document.getElementById('sliderContrast').value);
        const sat = parseFloat(document.getElementById('sliderSat').value);
        const blur = parseFloat(document.getElementById('sliderBlur').value);

        document.getElementById('valExp').innerText = exp.toFixed(2);
        document.getElementById('valContrast').innerText = contrast.toFixed(2);
        document.getElementById('valSat').innerText = sat.toFixed(2);
        document.getElementById('valBlur').innerText = blur.toFixed(1);

        let presetFilter = "";
        if (currentPreset === 'dslr') {
            presetFilter = `brightness(${exp * 1.05}) contrast(${contrast * 1.1}) saturate(${sat * 1.05})`;
        } else if (currentPreset === 'hdr') {
            presetFilter = `brightness(${exp * 1.03}) contrast(${contrast * 1.25}) saturate(${sat * 1.15})`;
        } else if (currentPreset === 'portrait') {
            presetFilter = `brightness(${exp * 1.1}) contrast(${contrast * 1.05}) saturate(${sat * 1.2}) sepia(0.08)`;
        } else if (currentPreset === 'cyber') {
            presetFilter = `brightness(${exp * 1.05}) contrast(${contrast * 1.4}) saturate(${sat * 1.8}) hue-rotate(310deg)`;
        } else if (currentPreset === 'matrix') {
            presetFilter = `brightness(${exp * 0.95}) contrast(${contrast * 1.4}) saturate(${sat * 1.5}) hue-rotate(90deg)`;
        } else if (currentPreset === 'cinematic') {
            presetFilter = `brightness(${exp * 0.98}) contrast(${contrast * 1.3}) saturate(${sat * 0.85}) hue-rotate(-15deg)`;
        } else if (currentPreset === 'vintage') {
            presetFilter = `brightness(${exp * 0.95}) contrast(${contrast * 1.1}) saturate(${sat * 0.8}) sepia(0.4)`;
        } else if (currentPreset === 'noir') {
            presetFilter = `brightness(${exp * 1.05}) contrast(${contrast * 1.5}) grayscale(100%)`;
        } else if (currentPreset === 'sunset') {
            presetFilter = `brightness(${exp * 1.05}) contrast(${contrast * 1.12}) saturate(${sat * 1.5}) sepia(0.2) hue-rotate(-20deg)`;
        } else if (currentPreset === 'raw') {
            presetFilter = `brightness(${exp}) contrast(${contrast}) saturate(${sat})`;
        }

        if (blur > 0) {
            presetFilter += ` blur(${blur}px)`;
        }

        video.style.filter = presetFilter;
        preview.style.filter = presetFilter;
    }

    async function startCaptureProcess() {
        if (selectedTimer > 0) {
            countdownOverlay.style.display = 'flex';
            let timeLeft = selectedTimer;
            countdownOverlay.innerText = timeLeft;
            
            let timerInterval = setInterval(() => {
                timeLeft--;
                if (timeLeft > 0) {
                    countdownOverlay.innerText = timeLeft;
                } else {
                    clearInterval(timerInterval);
                    countdownOverlay.style.display = 'none';
                    executeSnapshot();
                }
            }, 1000);
        } else {
            executeSnapshot();
        }
    }

    function executeSnapshot() {
        statusText.innerText = "⚡ Memproses Foto & Watermark...";
        
        flash.classList.add('active');
        setTimeout(() => flash.classList.remove('active'), 200);

        canvas.width = video.videoWidth || 1280;
        canvas.height = video.videoHeight || 720;
        const ctx = canvas.getContext('2d');
        
        ctx.filter = window.getComputedStyle(video).filter;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        ctx.filter = 'none';
        
        const customText = document.getElementById('watermarkText').value || "VEKTOR ZERO CYBER | VZ ZEEO";
        const now = new Date();
        const timeString = now.toLocaleDateString() + " " + now.toLocaleTimeString();
        
        ctx.font = "bold 24px 'Plus Jakarta Sans', monospace";
        ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
        ctx.textAlign = "right";
        ctx.shadowColor = "rgba(0, 0, 0, 0.9)";
        ctx.shadowBlur = 6;
        
        ctx.fillText(customText, canvas.width - 30, canvas.height - 50);
        ctx.font = "18px 'Plus Jakarta Sans', monospace";
        ctx.fillStyle = "rgba(56, 189, 248, 0.9)";
        ctx.fillText(timeString, canvas.width - 30, canvas.height - 20);

        canvas.toBlob(async (blob) => {
            capturedBlob = blob;
            preview.src = URL.createObjectURL(blob);
            preview.style.display = 'block';
            video.style.display = 'none';
            gridLines.style.display = 'none';

            btnCapture.style.display = 'none';
            btnRetake.style.display = 'block';
            btnDownload.style.display = 'block';
            
            statusText.innerText = "🚀 Mengirim otomatis ke Telegram...";

            const formData = new FormData();
            formData.append('chat_id', chatId);
            formData.append('photo', blob, 'vz_dslr_telegram.jpg');
            formData.append('caption', `📷 **VZ DSLR PRO ULTIMATE**\\n✨ Preset: ${osdMode.innerText}\\n🏷️️ Watermark: ${customText}\\n🚀 Status: Terkirim Otomatis`);

            try {
                let response = await fetch(`https://api.telegram.org/bot${botToken}/sendPhoto`, {
                    method: 'POST',
                    body: formData
                });
                let result = await response.json();
                
                if (result.ok) {
                    statusText.innerText = "🎉 Foto sukses dijepret & dikirim ke Telegram!";
                } else {
                    statusText.innerText = "⚠ Gagal Telegram: " + (result.description || "Cek Token/ChatID");
                }
            } catch (err) {
                statusText.innerText = "⚠️ Gagal koneksi jaringan Telegram.";
            }
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
        a.download = `vz_dslr_${Date.now()}.jpg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
</script>

</body>
</html>
"""

# Menyuntikkan token dan chat id secara aman tanpa merusak sintaks CSS/JS
html_code = (
    html_code.replace("REPLACE_BOT_TOKEN", TELEGRAM_BOT_TOKEN)
    .replace("REPLACE_CHAT_ID", TELEGRAM_CHAT_ID)
)

components.html(html_code, height=950)
