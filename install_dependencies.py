import sys
import urllib.request
import subprocess
import os

def install_dependencies():
    # Detect Python version
    major = sys.version_info.major
    minor = sys.version_info.minor
    print(f"Detected Python {major}.{minor}")
    
    # Check if 64-bit Windows
    is_64bit = sys.maxsize > 2**32
    if sys.platform != "win32" or not is_64bit:
        print("This script is intended for 64-bit Windows systems.")
        return

    # Map Python versions to the wheels in z-mahmud22/Dlib_Windows_Python3.x
    wheels = {
        (3, 7): "dlib-19.22.99-cp37-cp37m-win_amd64.whl",
        (3, 8): "dlib-19.22.99-cp38-cp38-win_amd64.whl",
        (3, 9): "dlib-19.22.99-cp39-cp39-win_amd64.whl",
        (3, 10): "dlib-19.22.99-cp310-cp310-win_amd64.whl",
        (3, 11): "dlib-19.24.1-cp311-cp311-win_amd64.whl",
        (3, 12): "dlib-19.24.99-cp312-cp312-win_amd64.whl",
        (3, 13): "dlib-20.0.99-cp313-cp313-win_amd64.whl",
        (3, 14): "dlib-20.0.99-cp314-cp314-win_amd64.whl",
    }
    
    version_key = (major, minor)
    if version_key not in wheels:
        print(f"No precompiled wheel found for Python {major}.{minor} in the repository. Trying regular install...")
        return
        
    wheel_name = wheels[version_key]
    url = f"https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/{wheel_name}"
    
    print(f"Downloading {wheel_name} from {url}...")
    try:
        # Use a user-agent header to avoid being blocked
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response, open(wheel_name, 'wb') as out_file:
            out_file.write(response.read())
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading wheel: {e}")
        return
        
    # Install the wheel
    print(f"Installing {wheel_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", wheel_name])
        print("dlib installed successfully!")
    except Exception as e:
        print(f"Failed to install dlib wheel: {e}")
        return
    finally:
        # Clean up the downloaded wheel file
        if os.path.exists(wheel_name):
            try:
                os.remove(wheel_name)
            except Exception:
                pass
            
    # Install the rest of requirements.txt
    print("Installing remaining requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All dependencies installed successfully!")
    except Exception as e:
        print(f"Failed to install requirements.txt: {e}")

if __name__ == "__main__":
    install_dependencies()
