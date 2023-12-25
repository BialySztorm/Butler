import subprocess
import platform
import sys


# Function to build executables for Linux
def build_for_linux():
    build_command = "python -m PyInstaller --onefile --icon=Butler.ico Butler.py"
    try:
        # skipcq: BAN-B602
        subprocess.run(build_command, shell=True, check=True)
        print("Linux executables built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building executables on Linux: {e}")


# Function to build executables for macOS
def build_for_mac():
    build_command = "python -m PyInstaller --onefile --icon=Butler.ico Butler.py"
    try:
        # skipcq: BAN-B602
        subprocess.run(build_command, shell=True, check=True)
        print("Executables on macOS built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building executables on macOS: {e}")


# Function to build executables for Windows
def build_for_windows():
    build_command = "python -m PyInstaller --onefile --version-file=Version.txt --icon=Butler.ico Butler.py"
    try:
        # skipcq: BAN-B602
        subprocess.run(build_command, shell=True, check=True)
        print("Windows executables built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building executables on Windows: {e}")


# Determine the operating system
system = platform.system()
# Choose the appropriate build function based on the detected operating system
if system == "Linux":
    build_for_linux()
elif system == "Darwin":
    build_for_mac()
elif system == "Windows":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    build_for_windows()
else:
    print("Unsupported operating system.")
