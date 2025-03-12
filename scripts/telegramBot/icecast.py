from flask import Flask, request, jsonify
import os
import subprocess
import yt_dlp
from dotenv import load_dotenv

app = Flask(__name__)

# Configuración de Icecast
load_dotenv()  # Carga las variables del archivo .env

# Ruta local para guardar los archivos descargados
DOWNLOAD_DIR = "/songs"
PLAYLIST_FILE = "/songs/list.txt"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route("/process_audio", methods=["POST"])
def process_audio():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Descargar el audio con yt-dlp en formato Ogg Vorbis
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'vorbis',
                'preferredquality': '5',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            output_file = ydl.prepare_filename(result).replace(".webm", ".ogg").replace(".m4a", ".ogg")
            final_path = os.path.join(DOWNLOAD_DIR, os.path.basename(output_file))
            os.rename(output_file, final_path)

        # Agregar la ruta del archivo a la playlist
        with open(PLAYLIST_FILE, "a") as playlist:
            playlist.write(final_path + "\n")

        stream_link = f"https://fondomarcador.com/icecast/"
        return jsonify({"stream_link": stream_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
