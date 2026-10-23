# save as install_deps.py
import subprocess
import sys

def install_packages():
    """Install all required packages"""
    
    packages = [
        "gtts",           # Text-to-speech
        "moviepy",        # Video editing
        "Pillow",         # Image creation
        "numpy",          # Required by moviepy
        "requests",       # For downloading assets
    ]
    
    print("Installing required packages...")
    
    for package in packages:
        print(f"\nInstalling {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
    
    print("\n" + "="*50)
    print("NEXT STEP: Install FFmpeg")
    print("="*50)
    print("""
    For macOS:
      brew install ffmpeg
    
    For Ubuntu/Debian:
      sudo apt update
      sudo apt install ffmpeg
    
    For Windows:
      1. Download from: https://ffmpeg.org/download.html
      2. Extract to C:\\ffmpeg
      3. Add C:\\ffmpeg\\bin to PATH environment variable
    
    OR use moviepy's auto-download (may not work for all):
      pip install imageio[ffmpeg]
    """)

if __name__ == "__main__":
    install_packages()