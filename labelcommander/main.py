import logging

from . import output
from . import render

logger = logging.getLogger(__name__)


def print_label(text):
    try:
        tex_path = render.generate(text)
        pdf_path = output.pdftex(tex_path)
        logger.info(pdf_path)
        # output.print(pdf_path)
    except output.PrintError as e:
        logger.error('Could not print label: %s', e)
        return False
    else:
        logger.debug('Printed label: %s', text)
        return True
