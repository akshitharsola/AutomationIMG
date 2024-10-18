from setuptools import setup, find_packages

setup(
    name="automationimg",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "scikit-image>=0.18.0",
        "matplotlib>=3.3.0",
        "tqdm>=4.50.0",
        "Pillow>=8.0.0",
        "torch>=1.7.0",
        "torchvision>=0.8.0",
        "pandas>=1.1.0",
        "scipy>=1.5.0",
        "ultralytics>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "automationimg=automationimg.main:main",
        ],
    },
    # Add other metadata as needed
    author="Akshit Harsola",
    author_email="harsolaakshit@gmail.com",
    description="A tool for image preprocessing and object detection",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/akshitharsola/AutomationIMG",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)