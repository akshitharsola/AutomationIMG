import os
import cv2
import json
import numpy as np
from ultralytics import YOLO
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_class_labels(path):
    with open(path, 'r') as f:
        return set(json.load(f))

def load_yolo_model(model_path='yolov5su.pt'):
    return YOLO(model_path)

def filter_detections_by_category(detections, class_labels, model):
    filtered_detections = []
    for *xyxy, conf, cls in detections:
        class_name = model.names[int(cls)]
        if class_name in class_labels:
            filtered_detections.append((*xyxy, conf, cls))
    return filtered_detections
    def batch_process_images(input_folder, output_folder):
    # function code here
        pass

def preprocess_images(input_folder, output_folder):
    # function code here
        pass

def process_image(image_path, model, class_labels, conf_threshold=0.25):
    image = cv2.imread(image_path)
    results = model(image)[0]
    detections = results.boxes.data.cpu().numpy()
    
    filtered_detections = filter_detections_by_category(detections, class_labels, model)
    
    annotations = []
    for *xyxy, conf, cls in filtered_detections:
        if conf >= conf_threshold:
            x1, y1, x2, y2 = map(int, xyxy)
            class_name = model.names[int(cls)]
            annotations.append({
                "label": class_name,
                "coordinates": {
                    "x": x1,
                    "y": y1,
                    "width": x2 - x1,
                    "height": y2 - y1
                },
                "confidence": float(conf)
            })
    
    return annotations, image

def save_visualization(image, annotations, output_path):
    for ann in annotations:
        x = ann['coordinates']['x']
        y = ann['coordinates']['y']
        w = ann['coordinates']['width']
        h = ann['coordinates']['height']
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, f"{ann['label']} {ann['confidence']:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imwrite(output_path, image)

def process_dataset(input_folder, output_folder, class_labels_path, conf_threshold=0.25):
    model = load_yolo_model()
    class_labels = load_class_labels(class_labels_path)
    
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, 'multiple_object_visualizations'), exist_ok=True)
    
    all_annotations = []
    
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        logging.warning("No images found in the input folder.")
        yield 0, 0
        return

    total_images = len(image_files)
    for i, filename in enumerate(image_files):
        image_path = os.path.join(input_folder, filename)
        annotations, image = process_image(image_path, model, class_labels, conf_threshold)
        
        if annotations:
            all_annotations.append({
                "image": filename,
                "annotations": annotations
            })
            
            vis_path = os.path.join(output_folder, 'multiple_object_visualizations', f'vis_{filename}')
            save_visualization(image, annotations, vis_path)
        
        yield i + 1, total_images
    
    annotations_path = os.path.join(output_folder, 'multiple_object_annotations.json')
    with open(annotations_path, 'w') as f:
        json.dump(all_annotations, f, indent=2)
    
    logging.info(f"Annotations saved to: {annotations_path}")
    
    generate_summary_report(all_annotations, total_images, output_folder)

def generate_summary_report(annotations, total_images, output_folder):
    successful_images = len(annotations)
    
    report = f"""
    Multiple Object Detection Summary Report
    ---------------------------------------
    Total images processed: {total_images}
    Images with detections: {successful_images}
    """
    
    if total_images > 0:
        percentage_successful = (successful_images / total_images) * 100
        report += f"Percentage of images with detections: {percentage_successful:.2f}%\n"
    else:
        report += "Percentage of images with detections: N/A (no images processed)\n"
    
    report += "\nObject type breakdown:\n"
    
    object_type_counts = {}
    for annotation in annotations:
        for obj in annotation['annotations']:
            label = obj['label']
            object_type_counts[label] = object_type_counts.get(label, 0) + 1
    
    if object_type_counts:
        for object_type, count in object_type_counts.items():
            report += f"    {object_type}: {count}\n"
    else:
        report += "    No objects detected\n"
    
    with open(os.path.join(output_folder, 'multiple_object_summary_report.txt'), 'w') as f:
        f.write(report)

if __name__ == "__main__":
    input_folder = "/path/to/preprocessed/images"
    output_folder = "/path/to/output"
    class_labels_path = "/path/to/class_labels.json"
    for progress, total in process_dataset(input_folder, output_folder, class_labels_path):
        print(f"Processing images: {progress}/{total}")
        