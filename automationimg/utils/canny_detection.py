# At the start of each .py file:
"""
AutomationIMG - A tool for automated image preprocessing and object detection
Copyright (C) 2024 Akshit Harsola

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import cv2
import numpy as np
import os
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_image(image_path):
    return cv2.imread(image_path)

def preprocess_image(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

def canny_edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

def create_bounding_boxes(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = 100
    significant_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in significant_contours]
    return bounding_boxes

def assess_image_quality(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    sharpness = np.var(laplacian)
    contrast = gray.std()
    sharpness_threshold = 50
    contrast_threshold = 30
    quality_score = (sharpness / sharpness_threshold + contrast / contrast_threshold) / 2
    return quality_score, f"Quality: {quality_score:.2f} (Sharpness={sharpness:.2f}, Contrast={contrast:.2f})"

def parse_filename(filename):
    match = re.match(r'(\w+)_(\d+)\.', filename)
    if match:
        return match.group(1), int(match.group(2))
    return None, None

def process_image(args):
    image_path, output_folder = args
    try:
        filename = os.path.basename(image_path)
        object_type, _ = parse_filename(filename)
        if object_type is None:
            logging.error(f"Unable to parse filename: {filename}")
            return None, True, filename

        original = load_image(image_path)
        quality_score, quality_message = assess_image_quality(original)
        
        preprocessed = preprocess_image(original)
        edges = canny_edge_detection(preprocessed)
        bounding_boxes = create_bounding_boxes(edges)
        
        annotation = {
            "image": filename,
            "quality_score": quality_score,
            "quality_message": quality_message,
            "annotations": []
        }
        
        is_difficult = quality_score < 1 or len(bounding_boxes) != 1
        
        if len(bounding_boxes) > 0:
            x, y, w, h = max(bounding_boxes, key=lambda box: box[2] * box[3])
            
            annotation["annotations"].append({
                "label": object_type,
                "coordinates": {
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                }
            })
            
            vis_image = original.copy()
            cv2.rectangle(vis_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imwrite(os.path.join(output_folder, 'single_object_bounding_boxes', filename), vis_image)
        
        cv2.imwrite(os.path.join(output_folder, 'single_object_edge_detection', filename), edges)
        
        return annotation, is_difficult, filename
    
    except Exception as e:
        logging.error(f"Error processing {image_path}: {str(e)}")
        return None, True, os.path.basename(image_path)


def batch_process_images(input_folder, output_folder, num_workers=4):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for subdir in ['single_object_edge_detection', 'single_object_bounding_boxes']:
        os.makedirs(os.path.join(output_folder, subdir), exist_ok=True)
    
    image_files = [
        (os.path.join(input_folder, f), output_folder)
        for f in os.listdir(input_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    
    if not image_files:
        logging.warning("No images found in the input folder.")
        yield 0, 0
        return

    annotations = []
    difficult_images = []
    total_images = len(image_files)
    difficult_count = 0
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_image = {executor.submit(process_image, args): args for args in image_files}
        for i, future in enumerate(as_completed(future_to_image)):
            result = future.result()
            if result:
                annotation, is_difficult, filename = result
                if annotation:
                    annotations.append(annotation)
                if is_difficult:
                    difficult_images.append(filename)
                    difficult_count += 1
            yield i + 1, total_images
    
    annotations.sort(key=lambda x: x['quality_score'], reverse=True)
    
    with open(os.path.join(output_folder, 'single_object_annotations.json'), 'w') as f:
        json.dump(annotations, f, indent=2)
    
    with open(os.path.join(output_folder, 'single_object_difficult_images.txt'), 'w') as f:
        f.write('\n'.join(difficult_images))
    
    generate_summary_report(annotations, total_images, difficult_count, output_folder)

def generate_summary_report(annotations, total_images, difficult_count, output_folder):
    successful_images = len(annotations)
    
    report = f"""
    Single Object Detection Summary Report
    ---------------------------------------
    Total images processed: {total_images}
    Successfully annotated images: {successful_images}
    Images flagged as difficult: {difficult_count}
    """
    
    if total_images > 0:
        percentage_difficult = (difficult_count / total_images) * 100
        report += f"Percentage of difficult images: {percentage_difficult:.2f}%\n"
    else:
        report += "Percentage of difficult images: N/A (no images processed)\n"
    
    report += "\nObject type breakdown:\n"
    
    object_type_counts = defaultdict(int)
    for annotation in annotations:
        for obj in annotation['annotations']:
            object_type_counts[obj['label']] += 1
    
    if object_type_counts:
        for object_type, count in object_type_counts.items():
            report += f"    {object_type}: {count}\n"
    else:
        report += "    No objects detected\n"
    
    with open(os.path.join(output_folder, 'single_object_summary_report.txt'), 'w') as f:
        f.write(report)

if __name__ == "__main__":
    input_folder = "/path/to/preprocessed/images"
    output_folder = "/path/to/output"
    for progress, total in batch_process_images(input_folder, output_folder):
        print(f"Processing images: {progress}/{total}")