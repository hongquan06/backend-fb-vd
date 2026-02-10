from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "videos")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/")
def home():
    return "Backend is running"


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing url"}), 400

    fb_url = data["url"]
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "outtmpl": filepath,
        "format": "best",
        "quiet": True,
        "nocheckcertificate": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([fb_url])

    return jsonify({
        "download_url": f"/file/{filename}"
    })


@app.route("/file/<name>")
def serve_file(name):
    path = os.path.join(DOWNLOAD_DIR, name)
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404

    return send_file(path, as_attachment=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


