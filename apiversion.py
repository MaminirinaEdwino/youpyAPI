import os
import yt_dlp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

front = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
  padding: 0;
  margin: 0;
}

body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: sans-serif;
}
body > div {
  border: 3px solid black;
  border-radius: 10px;
  padding: 10px;
  margin: 1px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
body > div h2 {
  font-size: 20px;
  margin-bottom: 10px;
}
body > div div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 5px;
  width: 100%;
}
body > div div span {
  font-size: 15px;
  margin-right: 10px;
}
body > div div label {
  font-size: 15px;
  margin-right: 10px;
}
body > div div input {
  font-size: 15px;
  padding: 6px;
  border-radius: 5px;
  border: 1px solid black;
}
body > div div select {
  font-size: 15px;
  padding: 6px;
  border-radius: 5px;
  border: 1px solid black;
  width: 95%;
}
body > div button {
  font-size: 15px;
  padding: 6px;
  border-radius: 5px;
  border: none;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
}
body > div button:hover {
  background-color: #45a049;
}

.loader {
  height: 50px;
  width: fit-content;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
}
.loader div {
  height: 100%;
  width: 8px;
  border-radius: 10px;
  background-color: green;
  animation: loading 1s linear infinite;
}
@keyframes loading {
  0% {
    transform: scaleY(0);
  }
  50% {
    transform: scaleY(1);
  }
  100% {
    transform: scaleY(0);
  }
}

/*# sourceMappingURL=style.css.map */

    </style>
    <title>Document</title>
</head>

<body>
    <h1>Youpy</h1>
    <div>
        <h2>Video</h2>
        <div id="urldiv">
            <label for="url">Video Url</label>
            <input type="text" id="url" name="url" placeholder="Enter video URL" required>
        </div>
        <div id="qualitydiv">
            <label for="url">Video Quality</label>
            <select name="quality" id="quality">
                <option value="360">360p</option>
                <option value="480">480p</option>
                <option value="720">720p</option>
                <option value="1080">1080p</option>
            </select>
        </div>
        <button onclick="downloadvideo()">Download</button>
        <div>
            <div id="statusv"></div>
        </div>
    </div>
    <div>
        <h2>Audio</h2>
        <div id="audiourldiv">
            <label for="audiourl">Video Url</label>
            <input type="text" id="audiourl" name="url" placeholder="Enter video URL" required>
        </div>
        <button onclick="downloadaudio()">Download</button>
        <div>
            <div id="status"></div>
        </div>
    </div>
    <script>
        function downloadaudio() {
            const url = document.getElementById('audiourl').value;
            const status = document.getElementById('status');
            if (url != ""){
                status.innerHTML = `<div class="loader">
            <div style="animation-delay: 0ms;"></div>
            <div style="animation-delay: 100ms;"></div>
            <div style="animation-delay: 200ms;"></div>
            <div style="animation-delay: 300ms;"></div>
            <div style="animation-delay: 400ms;"></div>
        </div>`;
                disableButton();
            fetch('http://localhost:1628/audio/?url=' + url,)
                .then(response => response.json())
                .then(data => {
                    status.innerHTML = `Audio download complete.`;
                    enableButton();
                })
                .catch(error => {
                    console.error('Error:', error);
                    status.innerHTML = "Error downloading audio.";
                    enableButton();
                });
            }
        }
        function disableButton(){
            document.querySelectorAll('button').forEach(button => {
                button.disabled = true;
            });
        }
        function enableButton(){
            document.querySelectorAll('button').forEach(button => {
                button.disabled = false;
            });
        }
        function downloadvideo() {
            const url = document.getElementById('url').value;
            const quality = document.getElementById('quality').value;
            const statusv = document.getElementById('statusv');
            if (url != "") {
                statusv.innerHTML = `<div class="loader">
            <div style="animation-delay: 0ms;"></div>
            <div style="animation-delay: 100ms;"></div>
            <div style="animation-delay: 200ms;"></div>
            <div style="animation-delay: 300ms;"></div>
            <div style="animation-delay: 400ms;"></div>
        </div>`;
                disableButton();
                fetch('http://localhost:1628/video/?url=' + url + '&quality=' + quality,)
                    .then(response => response.json())
                    .then(data => {
                        statusv.innerHTML = `Video download complete.`;
                        enableButton();
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        statusv.innerHTML = "Error downloading video.";
                        enableButton();
                    });
            }
        }
    </script>
</body>

</html>
"""
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez par les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Méthodes HTTP autorisées
    allow_headers=["*"],  # En-têtes autorisés
)
@app.get("/")
async def root():
    """Retourne le code HTML"""
    return HTMLResponse(content=front, status_code=200)

@app.get("/video/")
async def DownLoadVideo(url: str, quality: int):
        """Télécharge une vidéo YouTube et retourne le chemin du fichier"""
        os.makedirs("downloads/video", exist_ok=True)
        ydl_opts = {"format": f"bestvideo[ext=mp4][height={quality}]+bestaudio/best", "outtmpl": f'downloads/video/%(title)s.mp4', "merge_output_format": "mp4"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(ydl_opts.get("outtmpl"))
            
@app.get("/audio/")
async def dowload_audio(url: str):
        """Télécharge une vidéo YouTube et retourne le chemin du fichier"""
        os.makedirs("downloads/audio", exist_ok=True)
        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"downloads/audio/%(title)s.%(ext)s",  # nom du fichier de sortie
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',     # ou 'wav', 'm4a', etc.
            'preferredquality': '320',   # qualité audio
        }],
        'videonotfound': 'ignore',
        'videonotavailable': 'ignore',
        'continuedownload': True,
    }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])