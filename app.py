from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

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
                return jsonify({"error": "Không lấy được link video"}), 400

        return jsonify({
            "video_url": video_url
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "error": str(e)
        }), 500
