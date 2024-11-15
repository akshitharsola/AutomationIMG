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
- git (for git-based installation methods)

## 💻 Installation

### Method 1: Using pip and git (Recommended)
```bash
# Install directly from GitHub
pip install git+https://github.com/akshitharsola/AutomationIMG.git
```

### Method 2: Using Virtual Environment
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

### Method 3: Manual Download
1. Download the ZIP file from GitHub:
   - Go to https://github.com/akshitharsola/AutomationIMG
   - Click the green "Code" button
   - Select "Download ZIP"
2. Extract the ZIP file
3. Open terminal/command prompt in the extracted folder
4. Run:
```bash
pip install .
```

### Method 4: Direct Installation
```bash
# 1. Clone the repository
git clone https://github.com/akshitharsola/AutomationIMG.git
cd AutomationIMG

# 2. Install dependencies and package
pip install -r requirements.txt
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

## 🗑️ Uninstallation

### Method 1: Using pip
```bash
pip uninstall automationimg -y
```

### Method 2: Using GUI
1. Launch the application: `automationimg`
2. Click the "Uninstall Tool" button
3. Follow the prompts

### Method 3: Complete Cleanup (Including git repository)
```bash
# 1. Uninstall the package
pip uninstall automationimg -y

# 2. Remove the git repository (if you cloned it)
# For Windows:
rd /s /q AutomationIMG

# For Linux/Mac:
rm -rf AutomationIMG

# 3. Clear pip cache (optional)
pip cache purge
```

### Method 4: Clean Virtual Environment
If you installed in a virtual environment:
```bash
# 1. Deactivate virtual environment
deactivate

# 2. Remove virtual environment folder
# For Windows:
rd /s /q venv

# For Linux/Mac:
rm -rf venv
```

### Troubleshooting Uninstallation

If you encounter issues during uninstallation:

1. **Permission Issues:**
   ```bash
   # For Windows (Run as Administrator):
   pip uninstall automationimg -y

   # For Linux/Mac:
   sudo pip uninstall automationimg -y
   ```

2. **Files Still Present:**
   - Check for remaining files in your Python environment:
     ```bash
     python -c "import automationimg; print(automationimg.__file__)"
     ```
   - Manually delete the directory if shown

3. **Package Still Accessible:**
   - Try cleaning pip's cache:
     ```bash
     pip cache purge
     pip uninstall automationimg -y
     ```

Note: After uninstallation, you may safely delete any remaining files in the installation directory.

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