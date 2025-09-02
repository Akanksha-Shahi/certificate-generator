# Certificate Platform

## 1. Preview Tool
Open `index.html` in your browser.  
- Upload `template.png` and `fonts/Allura-Regular.ttf`.  
- Enter participant name, adjust Y position and font size.  
- Download PNG.

## 2. Bulk Generation
```bash
pip install -r requirements.txt
python generate_certificates.py --excel participants.xlsx --template template.png --font fonts/Allura-Regular.ttf --font_size 120 --y 520 --zip
