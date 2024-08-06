import pytesseract
import difflib
import matplotlib.pyplot as plt
import cv2
import os
import time

pytesseract.pytesseract.tesseract_cmd = r'tess/tesseract.exe'

start_time = time.time()

text_folder = 'text'

extracted_texts = []
for text_file in os.listdir(text_folder):
    if text_file.endswith('.txt'):
        with open(os.path.join(text_folder, text_file), 'r', encoding='utf-8') as f:
            extracted_texts.append((text_file, f.read()))

new_image_folder = 'want_to_find'
new_image_files = [os.path.join(new_image_folder, f) for f in os.listdir(new_image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
new_image_path = new_image_files[0] if new_image_files else None

if new_image_path is not None:
    new_image = cv2.imread(new_image_path)
    if new_image is not None:
        new_text = pytesseract.image_to_string(new_image, lang='tha+eng')
        
        closest_match = None
        closest_similarity = None
        
        for filename, text in extracted_texts:
            similarity = difflib.SequenceMatcher(None, new_text, text).ratio()
            if closest_similarity is None or similarity > closest_similarity:
                closest_similarity = similarity
                closest_match = (filename, text, similarity)
        
        if closest_match:
            closest_filename = closest_match[0]
            closest_text = closest_match[1]
            closest_similarity = closest_match[2]
            
            print(f"Closest match is from {closest_filename} with similarity {closest_similarity:.2f}")
            print(f"Text:\n{closest_text}")
            
            original_image_path = os.path.join('image', os.path.splitext(closest_match[0])[0] + '.png')
            closest_image = cv2.imread(original_image_path)
            if closest_image is not None:
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Execution time: {execution_time:.2f} seconds")
                plt.imshow(cv2.cvtColor(closest_image, cv2.COLOR_BGR2RGB))
                plt.title(f'Closest match: {closest_filename}')
                plt.axis('off')
                plt.show()
            else:
                print(f"Cannot display {original_image_path}")
    else:
        print(f"Cannot read {new_image_path}")
else:
    print("No new image found or cannot read the image")