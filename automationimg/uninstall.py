# automationimg/uninstall.py

import os
import sys
import shutil
import subprocess

def get_package_directory():
    """Get the root directory of the installed package"""
    try:
        import automationimg
        return os.path.dirname(os.path.dirname(automationimg.__file__))
    except ImportError:
        return None

def uninstall():
    """Complete uninstallation of AutomationIMG"""
    try:
        # Get the installation directory
        package_dir = get_package_directory()
        
        if package_dir:
            print(f"Found installation directory: {package_dir}")
        
        # First, uninstall using pip
        print("\nUninstalling package...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "automationimg", "-y"])
        
        # Then, remove the package directory if it exists
        if package_dir and os.path.exists(package_dir):
            print(f"\nRemoving package directory: {package_dir}")
            try:
                shutil.rmtree(package_dir)
                print("Package directory removed successfully")
            except Exception as e:
                print(f"Error removing directory: {str(e)}")
                print("You may need to remove it manually")
        
        print("\nUninstallation completed!")
        print("\nNote: If you still see any files, you can manually delete them.")
        
    except Exception as e:
        print(f"\nError during uninstallation: {str(e)}")
        print("\nPlease try manual uninstallation:")
        print("1. Run: pip uninstall automationimg -y")
        print("2. Delete the project directory manually")

if __name__ == "__main__":
    response = input("Are you sure you want to uninstall AutomationIMG? (yes/no): ").lower()
    if response == 'yes':
        uninstall()
    else:
        print("Uninstallation cancelled.")