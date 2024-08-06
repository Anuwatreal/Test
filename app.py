from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import cv2
import pytesseract
import difflib
import shutil

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# กำหนดเส้นทางไปยัง tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'tess/tesseract.exe'

# โฟลเดอร์สำหรับเก็บไฟล์อัปโหลด
UPLOAD_FOLDER = 'static/uploads'
TEXT_FOLDER = 'static/text'
COMPARE_FOLDER = 'static/want_to_find'

# สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)
os.makedirs(COMPARE_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ลบไฟล์เก่าในโฟลเดอร์ uploads และ text
        for folder in [UPLOAD_FOLDER, TEXT_FOLDER]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                os.remove(file_path)
        
        # รับไฟล์รูปภาพที่อัปโหลด
        images = request.files.getlist('images')
        if images:
            for image in images:
                if image and image.filename:
                    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
                    image.save(image_path)

                    # ถอดข้อความจากรูปภาพ
                    text = extract_text(image_path)

                    # บันทึกข้อความลงในไฟล์ในโฟลเดอร์ text
                    text_filename = os.path.splitext(image.filename)[0] + '.txt'
                    text_path = os.path.join(TEXT_FOLDER, text_filename)
                    with open(text_path, 'w', encoding='utf-8') as f:
                        f.write(text)

            flash('File upload successful', 'message2')
        else:
            flash('No files uploaded', 'message')
    else:
        flash('No files uploaded', 'message')

    return render_template('index.html')


@app.route('/find', methods=['POST'])
def find():
    flash('File upload successful', 'message2')
    if 'compare_image' in request.files:
        compare_file = request.files['compare_image']
        if compare_file and compare_file.filename:
            # บันทึกไฟล์ไปยังโฟลเดอร์ static/want_to_find
            compare_image_path = os.path.join(COMPARE_FOLDER, compare_file.filename)
            compare_file.save(compare_image_path)
            
            # ถอดข้อความจากรูปภาพเพื่อการเปรียบเทียบ
            new_text = extract_text(compare_image_path)
            
            if new_text:
                # โหลดข้อมูลที่ถอดข้อความจากไฟล์ทั้งหมดในโฟลเดอร์ text
                extracted_texts = []
                for text_file in os.listdir(TEXT_FOLDER):
                    if text_file.endswith('.txt'):
                        with open(os.path.join(TEXT_FOLDER, text_file), 'r', encoding='utf-8') as f:
                            extracted_texts.append((text_file, f.read()))

                # ค้นหาข้อความที่ใกล้เคียงที่สุดในไฟล์ข้อความที่บันทึกไว้
                closest_match = None
                closest_similarity = None

                for filename, text in extracted_texts:
                    similarity = difflib.SequenceMatcher(None, new_text, text).ratio()
                    if closest_similarity is None or similarity > closest_similarity:
                        closest_similarity = similarity
                        closest_match = (filename, text, similarity)
                
                # จัดเก็บผลลัพธ์การเปรียบเทียบ
                if closest_match:
                    compare_result = {
                        'closest_filename': closest_match[0][:-4],  # ลบ .txt ออก
                        'similarity': f"{closest_match[2]:.2f}",
                    }
                    return render_template('index.html', compare_result=compare_result)
    return redirect(url_for('index'))

@app.route('/find_image/<filename>')
def find_image(filename):
    return send_from_directory(UPLOAD_FOLDER, f"{filename}.png")

def extract_text(image_path):
    image = cv2.imread(image_path)
    if image is not None:
        return pytesseract.image_to_string(image, lang='tha+eng')
    return None

if __name__ == '__main__':
    app.run(debug=True)
