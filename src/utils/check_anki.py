import psutil 
import logging
import requests
import subprocess
import os
import sys
import shutil

logger = logging.getLogger(__name__)

# Iterate over the list of processes through "psutil" and check if anki is running
def is_anki_running():
    process_name = "anki"

    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass 
    return False

# Checks if the AnkiConnect API (or any endpoint) is responding.
def is_endpoint_active(url="http://127.0.0.1:8765"):
    try:
        # We use a short timeout so the script doesn't hang if Anki is closed
        response = requests.get(url, timeout=2)

        if response.status_code == 200: # status code 200 means success
            logger.debug(f"AnkiConnect is active at {url}")
    except (requests.ConnectionError, requests.Timeout):
        logger.error(f"Error when connecting to {url}. Check if AnkiConnect plug-in is enabled and 'webBindAddress':'webBindPort' correspondes to {url}")

# Try to launch Anki in the background
def try_launch_anki():
    if is_anki_running():
        logger.error("Anki is already running, skipping launch")
        return
    try:
        logger.info("Anki not detected, attempting to launch...")
        if sys.platform == "win32":
            # Windows approach
            # The executable usually is under "C:\Users\YOUR_USERNAME\AppData\Local\Programs\Anki" directory
            user_home = os.path.expanduser("~")
            anki_path = os.path.join(user_home, "AppData", "Local", "Programs", "Anki", "anki.exe")

            # Validate path exits and is a file
            if not os.path.isfile(anki_path):
                raise FileNotFoundError(f"Anki not found at {anki_path}")
            if not anki_path.endswith("anki.exe"):
                raise ValueError("Invalid Anki path")

            logger.debug(anki_path)

            subprocess.Popen(
                [anki_path],
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
        else: 
            # Linux/macOS approach using start_new_session
            anki_path = shutil.which("anki")
            if not anki_path:
                raise FileNotFoundError("Anki not found in PATH")

            subprocess.Popen(
                [anki_path],
                start_new_session=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
    except (FileNotFoundError, PermissionError, OSError) as e:
        logger.error(f"Error launching Anki: {e}. Try running it manually")