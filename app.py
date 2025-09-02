from flask import Flask, render_template, request, send_file, url_for
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os, io, zipfile

app = Flask(__name__)

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Certificate generation route
@app.route("/generate", methods=["POST"])
def generate():
    file = request.files["excel"]
    df = pd.read_excel(file)

    # Create in-memory zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for _, row in df.iterrows():
            name = str(row["Name"]).strip()

            # Load certificate template
            img = Image.open(os.path.join("static", "template.png"))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(os.path.join("fonts", "Allura-Regular.ttf"), 100)

            # Place text at (x=800, y=620)
            draw.text((800, 620), name, font=font, fill="black")

            # Save image into memory
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # Add to zip
            zipf.writestr(f"{name}.png", img_bytes.getvalue())

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="certificates.zip",
        mimetype="application/zip"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
