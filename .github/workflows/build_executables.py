import subprocess
import platform

def build_for_linux():
    build_command = "python -m PyInstaller --onefile Butler.py"
    try:
        subprocess.run(build_command, shell=True, check=True)
        print("Pliki wykonywalne na Linux zbudowane pomyślnie.")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas budowania plików wykonywalnych na Linux: {e}")

def build_for_mac():
    build_command = "python -m PyInstaller --onefile Butler.py"
    try:
        subprocess.run(build_command, shell=True, check=True)
        print("Pliki wykonywalne na macOS zbudowane pomyślnie.")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas budowania plików wykonywalnych na macOS: {e}")

def build_for_windows():
    build_command = "python -m PyInstaller --onefile Butler.py"
    try:
        subprocess.run(build_command, shell=True, check=True)
        print("Pliki wykonywalne na Windows zbudowane pomyślnie.")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas budowania plików wykonywalnych na Windows: {e}")

# Wybór odpowiedniej sekcji w zależności od systemu
system = platform.system()
if system == "Linux":
    build_for_linux()
elif system == "Darwin":
    build_for_mac()
elif system == "Windows":
    build_for_windows()
else:
    print("Nieobsługiwany system operacyjny.")