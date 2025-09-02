import os
import argparse
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def generate_certificates(excel, template, font, font_size=100, y=620, out_dir="out", zip_output=False):
    # Load participant names
    df = pd.read_excel(excel)
    if "Name" not in df.columns:
        raise ValueError("Excel file must have a 'Name' column")

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Load template & font
    template_img = Image.open(template)
    cert_w, cert_h = template_img.size
    font = ImageFont.truetype(font, font_size)

    # Draw each certificate
    for name in df["Name"]:
        cert = template_img.copy()
        draw = ImageDraw.Draw(cert)

        # Center text horizontally
        text_w, text_h = draw.textbbox((0, 0), name, font=font)[2:]
        x = (cert_w - text_w) // 2

        draw.text((x, y), name, font=font, fill="black")  # you can change fill to other colors

        filename = f"{name.replace(' ', '_')}.png"
        cert.save(out_path / filename)

    # Optionally zip results
    if zip_output:
        import zipfile
        zip_name = out_path / "certificates.zip"
        with zipfile.ZipFile(zip_name, "w") as zipf:
            for file in out_path.glob("*.png"):
                zipf.write(file, file.name)
        print(f"All certificates zipped at {zip_name}")

    print(f"Certificates saved in {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", required=True, help="Excel file with participant names")
    parser.add_argument("--template", required=True, help="Certificate template image")
    parser.add_argument("--font", required=True, help="Allura-Regular.ttf path")
    parser.add_argument("--font_size", type=int, default=100)
    parser.add_argument("--y", type=int, default=620)
    parser.add_argument("--out", default="out")
    parser.add_argument("--zip", action="store_true")
    args = parser.parse_args()

    generate_certificates(args.excel, args.template, args.font, args.font_size, args.y, args.out, args.zip)
