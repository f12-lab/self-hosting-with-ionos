from flask import Flask, request, jsonify
import os
import yt_dlp
from dotenv import load_dotenv

app = Flask(__name__)

# Configuración de Icecast
load_dotenv()  # Carga las variables del archivo .env

# Ruta local para guardar los archivos descargados
DOWNLOAD_DIR = "/songs/"
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

            # Obtener el nombre base del archivo .ogg
            base_name = ydl.prepare_filename(result)
            ogg_name = os.path.splitext(base_name)[0] + ".ogg"
            final_path = ogg_name  # Ya está en DOWNLOAD_DIR

        # Leer contenido actual si existe
        if os.path.exists(PLAYLIST_FILE):
            with open(PLAYLIST_FILE, "r") as playlist:
                lines = playlist.read().splitlines()
        else:
            lines = []

        # Añadir si no existe
        if final_path not in lines:
            with open(PLAYLIST_FILE, "a") as playlist:
                playlist.write(final_path + "\n")
            print(f"[INFO] Añadido a la lista: {final_path}")
        else:
            print(f"[INFO] Ya existía en la lista: {final_path}")

        stream_link = f"https://fondomarcador.com/icecast/"
        return jsonify({"stream_link": stream_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)