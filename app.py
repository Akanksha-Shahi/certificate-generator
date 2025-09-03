from flask import Flask, render_template, request, send_file
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os, io, zipfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# ----------------- PREVIEW CERTIFICATE -----------------
@app.route("/preview", methods=["POST"])
def preview():
    if "excel" not in request.files:
        return "❌ No file uploaded for preview"
    
    file = request.files["excel"]
    if file.filename == "":
        return "❌ No file selected"
    
    # Save temporarily
    temp_excel = os.path.join("/tmp", file.filename)
    file.save(temp_excel)

    # Read Excel
    df = pd.read_excel(temp_excel)

    if "Name" not in df.columns:
        return "❌ Excel must have a 'Name' column"

    # Take first row for preview
    name = str(df.iloc[0]["Name"]).strip()

    # Load template
    img = Image.open("static/template.png")
    draw = ImageDraw.Draw(img)

    # Load font
    font_path = os.path.join("fonts", "Allura-Regular.ttf")
    font = ImageFont.truetype(font_path, 100)

    # Place sample name text
    draw.text((800, 620), name, font=font, fill="black")

    # Save in memory and send as response
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype="image/png")

# ----------------- GENERATE ALL CERTIFICATES -----------------
@app.route("/generate", methods=["POST"])
def generate():
    if "excel" not in request.files:
        return "❌ No file uploaded"
    
    file = request.files["excel"]
    if file.filename == "":
        return "❌ No file selected"
    
    # Save Excel temporarily
    temp_excel = os.path.join("/tmp", file.filename)
    file.save(temp_excel)

    # Read Excel file
    df = pd.read_excel(temp_excel)

    if "Name" not in df.columns:
        return "❌ Excel must have a 'Name' column"

    # Prepare in-memory ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for _, row in df.iterrows():
            name = str(row["Name"]).strip()

            # Load certificate template
            img = Image.open("static/template.png")
            draw = ImageDraw.Draw(img)

            # Use custom font
            font_path = os.path.join("fonts", "Allura-Regular.ttf")
            font = ImageFont.truetype(font_path, 100)

            # Place text (adjust X,Y for your template)
            draw.text((800, 620), name, font=font, fill="black")

            # Save image to memory
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            zipf.writestr(f"{name}.png", img_bytes.getvalue())

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="certificates.zip",
        mimetype="application/zip"
    )

if __name__ == "__main__":
    # Render requires 0.0.0.0 host
    app.run(host="0.0.0.0", port=5000)
