from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "videos"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    fb_url = data.get("url")

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "outtmpl": filepath,
        "format": "best",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([fb_url])

    return jsonify({
        "download_url": f"https://backend-fb-vd.onrender.com/file/{filename}"
    })


@app.route("/file/<name>")
def serve_file(name):
    path = os.path.join(DOWNLOAD_DIR, name)
    return send_file(path, as_attachment=True)
