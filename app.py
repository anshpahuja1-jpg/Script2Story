# app.py
from flask import Flask, render_template, request, send_file, jsonify
import os
import threading
import uuid
from parser import parse_script
from image_generator import generate_image
from pdf_builder import build_storyboard_pdf

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Track job status
jobs = {}

def generate_storyboard(job_id, script_path):
    """Runs in background thread"""
    try:
        jobs[job_id] = {"status": "parsing", "progress": 0}
        scenes = parse_script(script_path)
        total = len(scenes)
        
        images = []
        for i, scene in enumerate(scenes):
            jobs[job_id] = {"status": f"Generating scene {i+1} of {total}...", "progress": int((i/total)*80)}
            img = generate_image(scene, i)
            images.append(img)
        
        jobs[job_id] = {"status": "building PDF", "progress": 90}
        output_path = os.path.join(OUTPUT_FOLDER, f"{job_id}.pdf")
        build_storyboard_pdf(scenes, images, output_path)
        
        jobs[job_id] = {"status": "done", "progress": 100, "file": output_path}
    except Exception as e:
        jobs[job_id] = {"status": "error", "error": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    if "script" not in request.files:
        return "No file uploaded", 400
    file = request.files["script"]
    if file.filename == "":
        return "No file selected", 400
    
    job_id = str(uuid.uuid4())
    script_path = os.path.join(UPLOAD_FOLDER, f"{job_id}.txt")
    file.save(script_path)
    
    # Start background thread
    thread = threading.Thread(target=generate_storyboard, args=(job_id, script_path))
    thread.daemon = True
    thread.start()
    
    return render_template("progress.html", job_id=job_id)

@app.route("/status/<job_id>")
def status(job_id):
    job = jobs.get(job_id, {"status": "not found"})
    return jsonify(job)

@app.route("/download/<job_id>")
def download(job_id):
    job = jobs.get(job_id)
    if not job or job["status"] != "done":
        return "Not ready", 404
    return send_file(job["file"], as_attachment=True, download_name="storyboard.pdf")

if __name__ == "__main__":
    app.run(debug=True)