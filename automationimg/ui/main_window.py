"""
AutomationIMG - A tool for automated image preprocessing and object detection
Copyright (C) 2024 Akshit Harsola

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QFileDialog, QLabel, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import shutil
import json
import subprocess
from automationimg.utils import canny_detection, preprocessing
from automationimg.utils.canny_detection import batch_process_images as single_object_detection
from automationimg.utils.preprocessing import preprocess_images


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
        self.setFixedSize(400, 650)
        self.input_folder = ""
        self.output_folder = ""
        self.current_working_dir = ""
        self.processing_thread = None
        self.exit_requested = False
        
        # Initialize UI elements as class attributes
        self.input_btn = None
        self.output_btn = None
        self.preprocess_btn = None
        self.single_obj_btn = None
        self.multiple_obj_btn = None
        self.uninstall_btn = None  # Add this line
        self.progress_label = None
        self.progress_bar = None
        self.exit_btn = None
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create buttons
        self.input_btn = self.create_button("Input Folder")
        self.output_btn = self.create_button("Output Folder")
        self.preprocess_btn = self.create_button("Preprocess Dataset")
        self.single_obj_btn = self.create_button("Single Object Detection")
        self.multiple_obj_btn = self.create_button("Multiple Object Detection")
        self.uninstall_btn = self.create_button("Uninstall Tool")  # Add uninstall button
        self.exit_btn = self.create_button("Exit")
        
        # Add buttons to layout
        layout.addWidget(self.input_btn)
        layout.addWidget(self.output_btn)
        layout.addWidget(self.preprocess_btn)
        layout.addWidget(self.single_obj_btn)
        layout.addWidget(self.multiple_obj_btn)

        # Progress components
        self.progress_label = QLabel("Progress:")
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        
        # Add uninstall and exit buttons
        layout.addWidget(self.uninstall_btn)
        layout.addWidget(self.exit_btn)
        
        # Style multiple object detection button
        self.multiple_obj_btn.setStyleSheet("""
            QPushButton {
                background-color: #cccccc;
                border: none;
                color: #666666;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #cccccc;
            }
        """)
        
        self.uninstall_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        
# =============================================================================
#         # Add closeEvent handler for window close button
#         self.setWindowFlags(
#             self.windowFlags() | 
#             Qt.WindowCloseButtonHint | 
#             Qt.WindowMinimizeButtonHint
#         )
# =============================================================================

        # Connect buttons
        self.input_btn.clicked.connect(self.select_input_folder)
        self.output_btn.clicked.connect(self.select_output_folder)
        self.preprocess_btn.clicked.connect(self.run_preprocessing)
        self.single_obj_btn.clicked.connect(self.run_single_object_detection)
        self.multiple_obj_btn.clicked.connect(self.run_multiple_object_detection)
        self.uninstall_btn.clicked.connect(self.uninstall_tool)  # Connect uninstall button
        self.exit_btn.clicked.connect(self.handle_exit)

        # Initially disable buttons
        self.preprocess_btn.setEnabled(False)
        self.single_obj_btn.setEnabled(False)
        self.multiple_obj_btn.setEnabled(True)
        
        # Set window flags
        self.setWindowFlags(
            self.windowFlags() | 
            Qt.WindowCloseButtonHint | 
            Qt.WindowMinimizeButtonHint
        )

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
        # Disable exit button during processing
        self.exit_btn.setEnabled(False)
        self.progress_label.setText("Progress: Preprocessing...")
        self.processing_thread = ProcessingThread(preprocess_dataset, self.input_folder, self.output_folder)
        self.processing_thread.progress_update.connect(self.update_progress)
        self.processing_thread.finished.connect(self.preprocessing_finished)
        self.processing_thread.finished.connect(lambda: self.exit_btn.setEnabled(True))  # Re-enable exit button
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
            
        self.exit_btn.setEnabled(False)
        self.progress_label.setText("Progress: Running Single Object Detection...")
        self.processing_thread = ProcessingThread(single_object_detection, self.current_working_dir, self.output_folder)
        self.processing_thread.progress_update.connect(self.update_progress)
        self.processing_thread.finished.connect(self.single_object_detection_finished)
        self.processing_thread.finished.connect(lambda: self.exit_btn.setEnabled(True))
        self.processing_thread.start()

    def single_object_detection_finished(self):
        self.progress_label.setText("Progress: Single Object Detection completed")
        print("Single Object Detection completed successfully!")

    def run_multiple_object_detection(self):
        QMessageBox.information(
        self,
        "Feature Under Development",
        "Multiple object detection is currently under development and will be available in a future update. "
        "Please use single object detection for now.",
        QMessageBox.Ok
    )

    def multiple_object_detection_finished(self):
        pass

    def update_progress(self, current, total):
        progress = int((current / total) * 100)
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"Progress: {current}/{total}")
        
    def handle_exit(self):
        """Properly handle application exit with thread cleanup"""
        if self.processing_thread and self.processing_thread.isRunning():
            reply = QMessageBox.question(
                self,
                'Confirm Exit',
                'A process is still running. Are you sure you want to exit?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.cleanup_and_exit()
        else:
            self.cleanup_and_exit()
            
    def cleanup_and_exit(self):
        """Clean up resources and exit the application"""
        self.exit_requested = True
        
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.quit()
            if not self.processing_thread.wait(1000):
                self.processing_thread.terminate()
                self.processing_thread.wait()
        
        QApplication.quit()

    def closeEvent(self, event):
        """Handle window close event (X button)"""
        if not self.exit_requested:
            self.handle_exit()
            event.ignore()
        else:
            event.accept()
            
    def uninstall_tool(self):
        """Handle tool uninstallation"""
        reply = QMessageBox.question(
            self,
            'Confirm Uninstallation',
            'Are you sure you want to uninstall AutomationIMG?\n'
            'This will close the application and remove it from your system.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                import subprocess
                
                # Run pip uninstall directly
                subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "automationimg", "-y"])
                
                QMessageBox.information(
                    self,
                    'Uninstallation Complete',
                    'AutomationIMG has been uninstalled.\n\n'
                    'Note: If you installed from source, you may need to\n'
                    'manually delete the project directory.\n\n'
                    'The application will now close.',
                    QMessageBox.Ok
                )
                
                # Close the application
                self.cleanup_and_exit()
                
            except Exception as e:
                QMessageBox.warning(
                    self,
                    'Uninstallation Error',
                    f'Error during uninstallation: {str(e)}\n\n'
                    'Please try these steps:\n'
                    '1. Close the application\n'
                    '2. Run: pip uninstall automationimg -y\n'
                    '3. Delete the project folder if it exists',
                    QMessageBox.Ok
                )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())