import logging

from firebasedata import LiveData
import pyrebase

from . import output
from . import render
from . import settings

logger = logging.getLogger(__name__)

NAME = 'firebase'
DATABASE_URL = 'https://{}.firebaseio.com'.format(settings.FIREBASE_APP_NAME)
AUTH_DOMAIN = '{}.firebaseapp.com'.format(settings.FIREBASE_APP_NAME)
STORAGE_BUCKET = '{}.appspot.com'.format(settings.FIREBASE_APP_NAME)

firebase_config = {
    'apiKey': settings.FIREBASE_API_KEY,
    'authDomain': AUTH_DOMAIN,
    'databaseURL': DATABASE_URL,
    'storageBucket': STORAGE_BUCKET,
    'serviceAccount': settings.FIREBASE_KEY_PATH,
}

firebase_app = pyrebase.initialize_app(firebase_config)

live_data = LiveData(firebase_app, settings.FIREBASE_PRINT_QUEUE_PATH)


def handle_print_request(jobs):
    # Print each job and remember any that failed
    remaining_jobs = {
        job_id: job
        for (job_id, job)
        in jobs.items()
        if not print_label(job['text'])
    }

    # Reset the queue with any failed jobs, or an empty dict if all were successful
    live_data.set_data('/', remaining_jobs)


def print_label(text):
    try:
        tex_path = render.generate(text)
        pdf_path = output.pdftex(tex_path)
        output.print(pdf_path)
    except output.PrintError:
        return False
    else:
        return True


live_data.signal('/').connect(handle_print_request)


def listen():
    live_data.get_data()