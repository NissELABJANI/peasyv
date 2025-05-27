from flask import Flask, request, render_template, send_file, url_for
import subprocess
import os
import uuid
import glob
import time
import json
from ngram_metrics import ngram_metrics

app = Flask(__name__)

# Paths
YTDLP_CMD = "yt-dlp"
VTT_CLEANER = "vtt.py"
ALIGN_SCRIPT = "p2fa/align.py"

@app.route("/", methods=["GET", "POST"])
def index():
    metrics = None
    if request.method == "POST":
        url = request.form["video_url"]
        work_id = str(uuid.uuid4())
        os.makedirs(work_id, exist_ok=True)

        wav_path = os.path.join(work_id, "test.wav")
        txt_path = os.path.join(work_id, "test.txt")
        vtt_path = os.path.join(work_id, "test.en.vtt")
        textgrid_path = os.path.join(work_id, "result.TextGrid")
        metrics_path = os.path.join(work_id, "metrics.json")

        try:
            # Step 1: Download audio and subtitles
            subprocess.run([
                "python3", YTDLP_CMD,
                "-x", "--audio-format", "wav",
                "--write-auto-sub", "--sub-lang", "en",
                "-o", f"{work_id}/test.%(ext)s",
                url
            ], check=True)

            # Step 2: Check for subtitles
            vtt_files = []
            for _ in range(10):
                vtt_files = glob.glob(os.path.join(work_id, "*.vtt"))
                if vtt_files:
                    break
                time.sleep(0.5)

            if not vtt_files:
                return "<h3 style='color:red'>❌ Subtitles not found.</h3>", 400

            os.rename(vtt_files[0], vtt_path)

            # Step 3: Convert VTT to TXT
            subprocess.run(["python3", VTT_CLEANER, vtt_path, txt_path], check=True)

            # Step 4: Run alignment
            subprocess.run(["python3", ALIGN_SCRIPT, wav_path, txt_path, textgrid_path], check=True)

            # Step 5: Generate metrics
            metrics = ngram_metrics(txt_path, metrics_path)

            return render_template("index.html",
                                   download_ready=True,
                                   textgrid_url=url_for('download', filename=textgrid_path),
                                   wav_url=url_for('download', filename=wav_path),
                                   txt_url=url_for('download', filename=txt_path),
                                   metrics_url=url_for('download', filename=metrics_path),
                                   metrics=metrics)

        except subprocess.CalledProcessError as e:
            return f"<h3 style='color:red'>❌ An error occurred:<br><code>{e}</code></h3>", 500

    return render_template("index.html", download_ready=False, metrics=None)

@app.route("/download/<path:filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
