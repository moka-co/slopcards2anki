import psutil 
import logging
import requests

logger = logging.getLogger(__name__)

# Iterate over the list of processes through "psutil" and check if anki is running
def is_anki_running():
    process_name = "anki"

    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                logger.info("Anki is running")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass 
    logger.error("Anki is not running. Please start it before calling any other functions")
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
