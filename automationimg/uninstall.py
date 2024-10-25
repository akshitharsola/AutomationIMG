import os
import sys
import shutil
import subprocess

def get_package_directory():
    """Get the root directory of the installed package"""
    try:
        import automationimg
        package_dir = os.path.dirname(os.path.dirname(automationimg.__file__))
        return package_dir if os.path.exists(package_dir) else None
    except ImportError:
        return None

def get_current_directory():
    """Get the current script directory"""
    return os.path.dirname(os.path.abspath(__file__))

def uninstall():
    """Complete uninstallation of AutomationIMG"""
    try:
        print("Starting uninstallation process...")
        
        # First attempt pip uninstall
        print("\nUninstalling package...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "automationimg", "-y"])
        
        # Try to get package directory
        package_dir = get_package_directory()
        if package_dir:
            print(f"\nRemoving package directory: {package_dir}")
            try:
                shutil.rmtree(package_dir)
                print("Package directory removed successfully")
            except Exception as e:
                print(f"Note: Could not remove directory automatically: {str(e)}")
                print(f"You may need to manually remove: {package_dir}")
        
        print("\nUninstallation completed!")
        return True
        
    except Exception as e:
        print(f"\nError during uninstallation: {str(e)}")
        print("\nPlease try manual uninstallation:")
        print("1. Run: pip uninstall automationimg -y")
        print("2. Delete the project directory manually")
        return False

if __name__ == "__main__":
    response = input("Are you sure you want to uninstall AutomationIMG? (yes/no): ").lower()
    if response == 'yes':
        uninstall()
    else:
        print("Uninstallation cancelled.")