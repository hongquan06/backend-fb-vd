from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend FB Video Downloader is running"

@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Missing url"}), 400

        fb_url = data["url"]

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format": "best",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(fb_url, download=False)
            video_url = info.get("url")

        if not video_url:
            return jsonify({"error": "Cannot extract video url"}), 400

        return jsonify({"video_url": video_url})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


# 🔴 CỰC KỲ QUAN TRỌNG CHO RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
