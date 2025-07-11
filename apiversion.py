import os
import yt_dlp
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez par les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # Méthodes HTTP autorisées
    allow_headers=["*"],  # En-têtes autorisés
)

app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="template")


@app.get("/")
async def default(request: Request):
  return template.TemplateResponse("index.html", context={"request": request})
  

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