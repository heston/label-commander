import logging
import os
import sys

# The name of the Firebase app, used to construct the REST URL.
FIREBASE_APP_NAME = os.getenv('LC_FIREBASE_APP_NAME', 'label-commander')

# Path to service account credentials file
FIREBASE_KEY_PATH = os.getenv('LC_FIREBASE_KEY_PATH', '/home/pi/.firebasekey')

# Firebase web API key
FIREBASE_API_KEY = os.getenv('LC_FIREBASE_API_KEY')

# Firebase Realtime Database URL
FIREBASE_DATABASE_URL = os.getenv('LC_FIREBASE_DATABASE_URL')

# The path to the print queue collection in the database
FIREBASE_PRINT_QUEUE_PATH = 'print_jobs'

# The name of the printer in CUPS
CUPS_PRINTER_NAME = os.getenv('LC_CUPS_PRINTER_NAME')

# Logging
LOG_LEVEL = os.getenv('LC_LOGGING_LEVEL', 'DEBUG')

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
    level=LOG_LEVEL,
    stream=sys.stdout
)
