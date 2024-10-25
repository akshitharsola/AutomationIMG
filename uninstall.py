# Create a new file: uninstall.py in your project root

import os
import shutil
import sys
import subprocess

def uninstall_tool():
    """Complete uninstallation of AutomationIMG"""
    try:
        # 1. Get the installation directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        
        # 2. Run pip uninstall
        print("Uninstalling AutomationIMG package...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "automationimg", "-y"])
        
        # 3. Remove the project directory
        print("Removing project files...")
        if os.path.exists(parent_dir):
            shutil.rmtree(parent_dir, ignore_errors=True)
            
        print("\nAutomationIMG has been completely uninstalled!")
        print("You can now delete the cloned repository folder if it still exists.")
        
    except Exception as e:
        print(f"Error during uninstallation: {str(e)}")
        print("\nPlease try manual removal:")
        print("1. Run: pip uninstall automationimg")
        print("2. Delete the project folder")

if __name__ == "__main__":
    response = input("Are you sure you want to completely remove AutomationIMG? (yes/no): ").lower()
    if response == 'yes':
        uninstall_tool()
    else:
        print("Uninstallation cancelled.")