from cachetools import TTLCache
from datetime import timedelta
import logging

from firebasedata import LiveData
import pyrebase

from . import main
from . import settings

logger = logging.getLogger(__name__)

NAME = 'firebase'
DATABASE_URL = 'https://{}.firebaseio.com'.format(settings.FIREBASE_APP_NAME)
AUTH_DOMAIN = '{}.firebaseapp.com'.format(settings.FIREBASE_APP_NAME)
STORAGE_BUCKET = '{}.appspot.com'.format(settings.FIREBASE_APP_NAME)
TTL = timedelta(minutes=75)
CACHE_SIZE = 20  # items
CACHE_TTL = 30  # seconds

firebase_config = {
    'apiKey': settings.FIREBASE_API_KEY,
    'authDomain': AUTH_DOMAIN,
    'databaseURL': DATABASE_URL,
    'storageBucket': STORAGE_BUCKET,
    'serviceAccount': settings.FIREBASE_KEY_PATH,
}
firebase_app = pyrebase.initialize_app(firebase_config)
live_data = LiveData(firebase_app, settings.FIREBASE_PRINT_QUEUE_PATH, TTL)
message_cache = TTLCache(CACHE_SIZE, CACHE_TTL)


def handle_print_request(sender, value=None, path=None):
    # Print each job and remember any that failed
    if value is None:
        return

    remaining_jobs = {}

    try:
        for (job_id, job) in value.items():
            if job_id in message_cache:
                # label already printed recently
                logger.info('Skipping duplicate print request: %s', job_id)
                continue

            success = main.print_label(job['text'], job.get('qty'))
            if success:
                # printing succeeded
                message_cache[job_id] = True
                logger.info('Printed successfully: %s', job_id)
            else:
                # printing failed
                remaining_jobs[job_id] = job
                logger.info('Printing failed: %s', job_id)
    except (AttributeError, KeyError) as e:
        logger.warning('Invalid print request: %s', e)
    else:
        # Reset the queue with any failed jobs,
        # or an empty dict if all were successful
        live_data.set_data('/', remaining_jobs)


live_data.signal('/').connect(handle_print_request)


def listen():
    live_data.get_data()
