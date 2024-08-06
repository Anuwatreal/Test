import cv2
import pytesseract
import difflib
import matplotlib.pyplot as plt
import os
import time

pytesseract.pytesseract.tesseract_cmd = r'tess/tesseract.exe'

start_time = time.time()

image_files = [os.path.join('image', f) for f in os.listdir('image') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

extracted_texts = []

for image_file in image_files:
    image = cv2.imread(image_file)
    if image is not None:
        text = pytesseract.image_to_string(image, lang='tha+eng')
        extracted_texts.append((image_file, text))
    else:
        print(f"Cannot read {image_file}")

new_image_files = [os.path.join('want_to_find', f) for f in os.listdir('want_to_find') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
new_image = new_image_files[0]

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
        
        closest_image = cv2.imread(closest_filename)
        if closest_image is not None:
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time:.2f} seconds")
            plt.imshow(cv2.cvtColor(closest_image, cv2.COLOR_BGR2RGB))
            plt.title(f'Closest match: {closest_filename[6:]}')
            plt.axis('off')
            plt.show()
        else:
            print(f"Cannot display {closest_filename}")
else:
    print(f"Cannot read {new_image}")