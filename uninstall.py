import subprocess
import sys
import os
import shutil

def uninstall():
    try:
        # Get the current script's directory (project root)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Uninstall using pip
        print("Uninstalling AutomationIMG...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "automationimg", "-y"])
        
        # Remove project directory
        parent_dir = os.path.dirname(current_dir)
        if os.path.exists(parent_dir):
            print(f"Removing project directory: {parent_dir}")
            shutil.rmtree(parent_dir, ignore_errors=True)
        
        print("\nUninstallation completed successfully!")
        print("You can now delete the remaining files manually if any exist.")
        
    except Exception as e:
        print(f"\nError during uninstallation: {str(e)}")
        print("\nPlease try manual uninstallation:")
        print("1. Run: pip uninstall automationimg -y")
        print("2. Delete the project directory manually")

if __name__ == "__main__":
    choice = input("Are you sure you want to uninstall AutomationIMG? (yes/no): ")
    if choice.lower() == 'yes':
        uninstall()
    else:
        print("Uninstallation cancelled.")