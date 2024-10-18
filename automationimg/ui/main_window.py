import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QFileDialog, QLabel, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import shutil
import json
from automationimg.utils import canny_detection, category_aware_detection, preprocessing
# Import the detection functions
from automationimg.utils.canny_detection import batch_process_images as single_object_detection
from automationimg.utils.category_aware_detection import batch_process_images as multiple_object_detection
from automationimg.utils.preprocessing import preprocess_images
# Update other imports as necessary

class ProcessingThread(QThread):
    progress_update = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, function, *args):
        super().__init__()
        self.function = function
        self.args = args

    def run(self):
        for progress, total in self.function(*self.args):
            self.progress_update.emit(progress, total)
        self.finished.emit()

def preprocess_dataset(input_folder, output_folder):
    processed_folder = os.path.join(output_folder, 'processed')
    os.makedirs(processed_folder, exist_ok=True)

    class_labels = set()
    total_images = 0
    processed_images = 0

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
                    source_path = os.path.join(root, file)
                    dest_path = os.path.join(processed_folder, f"{class_name}_{file}")
                    shutil.copy2(source_path, dest_path)
                    processed_images += 1
                    yield processed_images, total_images

    with open(os.path.join(output_folder, 'class_labels.json'), 'w') as f:
        json.dump(list(class_labels), f)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutomationIMG")
        self.setFixedSize(400, 500)
        self.input_folder = ""
        self.output_folder = ""
        self.current_working_dir = ""
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Folder selection buttons
        self.input_btn = self.create_button("Input Folder")
        self.output_btn = self.create_button("Output Folder")
        layout.addWidget(self.input_btn)
        layout.addWidget(self.output_btn)

        # Processing buttons
        self.preprocess_btn = self.create_button("Preprocess Dataset")
        self.single_obj_btn = self.create_button("Single Object Detection")
        self.multiple_obj_btn = self.create_button("Multiple Object Detection")
        
        layout.addWidget(self.preprocess_btn)
        layout.addWidget(self.single_obj_btn)
        layout.addWidget(self.multiple_obj_btn)

        # Progress
        self.progress_label = QLabel("Progress:")
        layout.addWidget(self.progress_label)
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Exit button
        self.exit_btn = self.create_button("Exit")
        layout.addWidget(self.exit_btn)

        # Connect buttons
        self.input_btn.clicked.connect(self.select_input_folder)
        self.output_btn.clicked.connect(self.select_output_folder)
        self.preprocess_btn.clicked.connect(self.run_preprocessing)
        self.single_obj_btn.clicked.connect(self.run_single_object_detection)
        self.multiple_obj_btn.clicked.connect(self.run_multiple_object_detection)
        self.exit_btn.clicked.connect(self.close)

        # Initially disable buttons
        self.preprocess_btn.setEnabled(False)
        self.single_obj_btn.setEnabled(False)
        self.multiple_obj_btn.setEnabled(False)

    def create_button(self, text):
        button = QPushButton(text)
        button.setFixedHeight(50)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        return button

    def select_input_folder(self):
        self.input_folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        self.check_folders_selected()

    def select_output_folder(self):
        self.output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        self.check_folders_selected()

    def check_folders_selected(self):
        if self.input_folder and self.output_folder:
            self.preprocess_btn.setEnabled(True)
        else:
            self.preprocess_btn.setEnabled(False)
            
    def set_input_folder(self, path):
        self.input_folder = path
        self.check_folders_selected()

    def set_output_folder(self, path):
        self.output_folder = path
        self.check_folders_selected()

    def run_preprocessing(self):
        if not self.input_folder or not self.output_folder:
            print("Error: Input and output folders must be set.")
            return
        self.progress_label.setText("Progress: Preprocessing...")
        self.processing_thread = ProcessingThread(preprocess_dataset, self.input_folder, self.output_folder)
        self.processing_thread.progress_update.connect(self.update_progress)
        self.processing_thread.finished.connect(self.preprocessing_finished)
        self.processing_thread.start()

    def preprocessing_finished(self):
        self.current_working_dir = os.path.join(self.output_folder, 'processed')
        self.progress_label.setText("Progress: Preprocessing completed")
        self.single_obj_btn.setEnabled(True)
        self.multiple_obj_btn.setEnabled(True)
        print("Preprocessing completed successfully!")

    def run_single_object_detection(self):
        if not self.current_working_dir or not self.output_folder:
            print("Error: Preprocessing must be run first.")
            return
        self.progress_label.setText("Progress: Running Single Object Detection...")
        self.processing_thread = ProcessingThread(single_object_detection, self.current_working_dir, self.output_folder)
        self.processing_thread.progress_update.connect(self.update_progress)
        self.processing_thread.finished.connect(self.single_object_detection_finished)
        self.processing_thread.start()

    def single_object_detection_finished(self):
        self.progress_label.setText("Progress: Single Object Detection completed")
        print("Single Object Detection completed successfully!")

    def run_multiple_object_detection(self):
        if not self.current_working_dir or not self.output_folder:
            print("Error: Preprocessing must be run first.")
            return
        class_labels_path = os.path.join(self.output_folder, 'class_labels.json')
        if not os.path.exists(class_labels_path):
            print("Warning: Class labels file not found. Run preprocessing first.")
            return
        self.progress_label.setText("Progress: Running Multiple Object Detection...")
        self.processing_thread = ProcessingThread(multiple_object_detection, self.current_working_dir, self.output_folder, class_labels_path)
        self.processing_thread.progress_update.connect(self.update_progress)
        self.processing_thread.finished.connect(self.multiple_object_detection_finished)
        self.processing_thread.start()

    def multiple_object_detection_finished(self):
        self.progress_label.setText("Progress: Multiple Object Detection completed")
        print("Multiple Object Detection completed successfully!")

    def update_progress(self, current, total):
        progress = int((current / total) * 100)
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"Progress: {current}/{total}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())