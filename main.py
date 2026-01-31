from ultralytics import YOLO
import os
import glob

# 1. Load the model
model = YOLO('helmet_detector_best.pt') 

# 2. Automatically find all images inside the 'datasets' folder
# We join the folder name with the extension patterns
search_path = os.path.join('datasets', '*')
image_extensions = ('.jpg', '.jpeg', '.png')
image_files = [f for f in glob.glob(search_path) if f.lower().endswith(image_extensions)]

if not image_files:
    print("No images found in the 'datasets' folder! Please move your images there.")
else:
    print(f"Clean Repo Mode: Found {len(image_files)} images in 'datasets'.")

# 3. Process every image
for img_path in image_files:
    print(f"\nProcessing: {os.path.basename(img_path)}")
    
    results = model.predict(
        source=img_path, 
        conf=0.20, 
        iou=0.70, 
        imgsz=1024, 
        save=True
    )

    # 4. Counting Logic
    for r in results:
        helmet_classes = ['1-2-helmet', '3-4-helmet', 'Full-face-helmet']
        no_helmet_classes = ['Face_and_Hair', 'Bald', 'Cap']
        
        wearing = 0
        not_wearing = 0
        
        for box in r.boxes:
            label = model.names[int(box.cls[0])]
            if label in helmet_classes:
                wearing += 1
            elif label in no_helmet_classes:
                not_wearing += 1
                
        print(f"RESULTS FOR {os.path.basename(img_path)}:")
        print(f"total person detected = {wearing + not_wearing}")
        print(f"wearing helmet = {wearing}")
        print(f"not wearing helmet = {not_wearing}")
        print("-" * 30)

print("\nBatch processing complete.")

# Add this at the very end of your main.py

import subprocess



# This opens the folder where the result was saved automatically

result_dir = os.path.abspath(results[0].save_dir)

os.startfile(result_dir)