import os
import shutil
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_dataset(input_folder, output_folder):
    processed_folder = os.path.join(output_folder, 'processed')
    os.makedirs(processed_folder, exist_ok=True)

    class_labels = set()
    total_images = 0
    processed_images = 0
    error_images = 0

    for root, _, files in os.walk(input_folder):
        class_name = os.path.basename(root)
        if class_name.lower() not in ['images', 'data', 'dataset']:
            class_labels.add(class_name)
            total_images += len([f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    for root, _, files in os.walk(input_folder):
        class_name = os.path.basename(root)
        if class_name.lower() not in ['images', 'data', 'dataset']:
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        source_path = os.path.join(root, file)
                        dest_path = os.path.join(processed_folder, f"{class_name}_{file}")
                        shutil.copy2(source_path, dest_path)
                        processed_images += 1
                        yield processed_images, total_images
                    except Exception as e:
                        logging.error(f"Error processing {file}: {str(e)}")
                        error_images += 1

    with open(os.path.join(output_folder, 'class_labels.json'), 'w') as f:
        json.dump(list(class_labels), f)

    logging.info("Preprocessing completed.")
    logging.info(f"Total images processed: {processed_images}")
    logging.info(f"Error images: {error_images}")
    logging.info(f"Total class labels: {len(class_labels)}")

def batch_process_images(input_folder, output_folder):
    # function code here
    pass

def preprocess_images(input_folder, output_folder):
    pass
    # function code here
    
if __name__ == "__main__":
    input_folder = "/path/to/input/folder"
    output_folder = "/path/to/output/folder"
    for progress, total in preprocess_dataset(input_folder, output_folder):
        print(f"Processing images: {progress}/{total}")