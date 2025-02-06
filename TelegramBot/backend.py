from flask import Flask, request, jsonify
import os
import subprocess
import yt_dlp

app = Flask(__name__)

# Ruta local para guardar los archivos descargados
DOWNLOAD_DIR = "/var/www/webpages/videos/hls"

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

        # Ruta para el archivo .m3u8
        hls_output = os.path.join(DOWNLOAD_DIR, "stream.m3u8")

        # Comando para generar HLS
        command = [
            "ffmpeg",
            "-i", output_file,         # Archivo de entrada
            "-c:v", "libx264",         # Recodifica el video a H.264
            "-preset", "veryfast",     # Optimiza la velocidad de recodificación
            "-b:v", "800k",            # Define un bitrate razonable
            "-c:a", "aac",             # Convierte el audio a AAC
            "-ar", "44100",            # Frecuencia de muestreo del audio
            "-ac", "1",                # Audio en mono
            "-f", "hls",               # Formato de salida HLS
            "-hls_time", "10",         # Duración de cada segmento .ts en segundos
            "-hls_list_size", "0",     # Guarda todos los segmentos en el .m3u8
            "-hls_segment_filename", os.path.join(DOWNLOAD_DIR, "segment_%03d.ts"),  # Nombre de los segmentos .ts
            hls_output                 # Archivo de lista de reproducción .m3u8
        ]
        subprocess.Popen(command)

        # URL base del servidor donde se alojará el video
        stream_link = f"https://fondomarcador.com/videos/"
        return jsonify({"stream_link": stream_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)