import cv2
import pytesseract
import os
import time
import shutil

pytesseract.pytesseract.tesseract_cmd = r'tess/tesseract.exe'

start_time = time.time()

image_folder = 'image'

text_folder = 'text'

if os.path.exists(text_folder):
    shutil.rmtree(text_folder)

os.makedirs(text_folder, exist_ok=True)

for image_file in os.listdir(image_folder):
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)
        if image is not None:
            text = pytesseract.image_to_string(image, lang='tha+eng')
            text_filename = os.path.splitext(image_file)[0] + '.txt'
            text_path = os.path.join(text_folder, text_filename)
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print(f"Cannot read {image_file}")
            
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
