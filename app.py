# app.py
from flask import Flask, render_template, request, send_file
import os
from parser import parse_script
from image_generator import generate_image
from pdf_builder import build_storyboard_pdf

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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
    
    # Save uploaded script
    script_path = os.path.join(UPLOAD_FOLDER, "script.txt")
    file.save(script_path)
    
    # Run pipeline
    scenes = parse_script(script_path)
    images = []
    for i, scene in enumerate(scenes):
        img = generate_image(scene, i)
        images.append(img)
    
    # Build PDF
    output_path = os.path.join(OUTPUT_FOLDER, "storyboard.pdf")
    build_storyboard_pdf(scenes, images, output_path)
    
    return send_file(output_path, as_attachment=True, download_name="storyboard.pdf")

if __name__ == "__main__":
    app.run(debug=True)