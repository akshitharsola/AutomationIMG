from setuptools import setup, find_packages

setup(
    name="automationimg",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
        # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "automationimg=automationimg.main:main",
        ],
    },
)