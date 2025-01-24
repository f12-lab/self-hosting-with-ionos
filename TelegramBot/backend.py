from flask import Flask, request, jsonify
import os
import subprocess
import yt_dlp

app = Flask(__name__)

# Ruta local para guardar los archivos descargados
DOWNLOAD_DIR = "/var/www/webpages/videos/"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route("/process", methods=["POST"])
def process_stream():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Descargar el video con yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',  # Selecciona mejor calidad
            'merge_output_format': 'mp4',  # Fuerza la salida como .mp4
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            output_file = ydl.prepare_filename(result)

        # Dirección de tu servidor RTMP
        rtmp_server = "rtmp://127.0.0.1:1935/live/fondovideo"

        # Transmitir con ffmpeg
        command = [
            "ffmpeg",
            "-re",                     # Lee el archivo en tiempo real
            "-i", output_file,         # Archivo descargado
            "-c:v", "libx264",         # Recodifica el video a H.264
            "-preset", "veryfast",     # Optimiza la velocidad de recodificación
            "-b:v", "800k",            # Define un bitrate razonable
            "-c:a", "aac",             # Convierte el audio a AAC
            "-ar", "44100",            # Frecuencia de muestreo del audio
            "-ac", "1",                # Audio en mono
            "-f", "flv",               # Formato de salida FLV
            rtmp_server,               # URL del servidor RTMP
        ]
        subprocess.Popen(command)

        # Retornar enlace al usuario
        stream_link = "rtmp://fondomarcador.com/live/fondovideo"
        return jsonify({"stream_link": stream_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
