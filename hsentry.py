import sys
import logging
from raven import Client

client = None
DEFAULT_URI = ''


def _handler(exc_type, exc_value, exc_traceback):

    if not issubclass(exc_type, KeyboardInterrupt):
        client.captureException(exc_info=(exc_type, exc_value, exc_traceback))

    sys.__excepthook__(exc_type, exc_value, exc_traceback)


def init(uri=DEFAULT_URI):

    try:
        global client
        client = Client(uri)
    except Exception as ex:
        logging.warning('failed to connect to sentry: ' + str(ex))
    else:
        sys.excepthook = _handler


def message(msg):
    client.captureMessage(msg)


def capture(*args, **kwargs):
    client.capture(*args, **kwargs)
