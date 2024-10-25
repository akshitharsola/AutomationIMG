
# AutomationIMG

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

AutomationIMG is a Python-based tool for automated image preprocessing and object detection, featuring an intuitive graphical user interface. It simplifies the process of organizing and analyzing image datasets for machine learning and computer vision tasks.

## 🚀 Features

- **Preprocessing Pipeline**
  - Automated image organization
  - Support for various directory structures
  - Batch processing capabilities

- **Object Detection**
  - Single object detection using Canny edge detection
  - Bounding box visualization
  - Quality assessment of detections

- **User Interface**
  - Intuitive GUI built with PyQt5
  - Real-time progress tracking
  - Easy folder selection and processing

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)

## 💻 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/akshitharsola/AutomationIMG.git
cd AutomationIMG
```

2. **Install the package:**
```bash
pip install -e .
```

## 📖 Usage

### Directory Structure
The tool supports the following directory structure for input data:
```
Main_Folder/
    └── Apple/
        └── image1.jpg
        └── image2.jpg
    └── Orange/
        └── image1.jpg
        └── image2.jpg
```

### Running the Tool
1. **Start the application:**
```python
# Simply run
automationIMG
```

2. **Using the GUI:**
   - Click "Input Folder" to select your image directory
   - Choose "Output Folder" for processed results
   - Run "Preprocess Dataset" to organize images
   - Use "Single Object Detection" for detection and analysis

### Output Structure
The tool generates the following output structure:
```
Output_Folder/
    └── processed/
        └── images
        └── annotations.json
    └── edge_detection/
        └── detection results
    └── bounding_boxes/
        └── visualizations
```
### 🗑️ Uninstallation

You have three ways to uninstall AutomationIMG:

1. **Using the GUI (Recommended)**
   - Launch the application
   - Click the "Uninstall Tool" button
   - Confirm the uninstallation
   - The tool will remove itself and close

2. **Using the uninstall script**
```bash
python uninstall.py
```

3. **Manual uninstallation**
```bash
pip uninstall automationimg -y
```

After uninstallation, you may safely delete the project folder if it still exists.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Akshit Harsola**
- Email: harsolaakshit@gmail.com
- GitHub: [@akshitharsola](https://github.com/akshitharsola)

## 🙏 Acknowledgments

- Thanks to all contributors who help improve this tool
- Special thanks to the open-source community for their valuable tools and libraries

## 📞 Support

If you encounter any problems or have suggestions, please [open an issue](https://github.com/akshitharsola/AutomationIMG/issues).
