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
Before installation, ensure you have:
- Python 3.7 or higher
- pip (Python package installer)
- git

## 💻 Installation

### Method 1: Using Virtual Environment (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/akshitharsola/AutomationIMG.git
cd AutomationIMG

# 2. Create and activate virtual environment
# For Windows:
python -m venv venv
venv\Scripts\activate

# For Linux/Mac:
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install the package in development mode
pip install -e .
```

### Method 2: Direct Installation
```bash
# 1. Clone the repository
git clone https://github.com/akshitharsola/AutomationIMG.git
cd AutomationIMG

# 2. Install dependencies and package
pip install -r requirements.txt
pip install -e .
```

### Method 3: Dependencies-Only Installation
If you're having issues with the full installation:

```bash
# 1. Clone the repository
git clone https://github.com/akshitharsola/AutomationIMG.git
cd AutomationIMG

# 2. Install core dependencies only
pip install PyQt5>=5.15.0 opencv-python>=4.5.0 numpy>=1.19.0 scikit-image>=0.18.0 matplotlib>=3.3.0 tqdm>=4.50.0 Pillow>=8.0.0 pandas>=1.1.0 scipy>=1.5.0

# 3. Install the package
pip install -e .
```

### Troubleshooting Installation

If you encounter installation issues:

1. **PyQt5 Installation Issues:**
   ```bash
   # Try installing PyQt5 separately first
   pip install PyQt5
   ```

2. **OpenCV Installation Issues:**
   ```bash
   # Try installing opencv-python-headless instead
   pip install opencv-python-headless
   ```

3. **Permission Issues:**
   - For Linux/Mac: Use `sudo pip install ...`
   - For Windows: Run command prompt as administrator

4. **Version Conflicts:**
   ```bash
   # Create a fresh virtual environment and try again
   python -m venv fresh_venv
   # Activate it and retry installation
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
```bash
automationimg
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

You have several options to uninstall AutomationIMG:

1. **Using the GUI**
   - Launch the application: `automationimg`
   - Click the "Uninstall Tool" button
   - Follow the prompts

2. **Using the uninstall module**
```bash
python -m automationimg.uninstall
```

3. **Manual uninstallation**
```bash
pip uninstall automationimg -y
```

Note: After uninstallation, any remaining files in the installation directory can be safely deleted manually.

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

## ⚙️ Compatibility

Tested and supported on:
- Windows 10/11
- Ubuntu 20.04/22.04
- macOS 11 (Big Sur) and later

Note: Some features may require additional system-specific configuration. Please check the troubleshooting section if you encounter any issues.