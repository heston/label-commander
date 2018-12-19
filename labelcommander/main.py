import logging

from . import formatter
from . import output
from . import render

logger = logging.getLogger(__name__)


def print_label(text, qty=None, date=None):
    try:
        filtered_text = formatter.process(text)
        logger.debug('Printing label: %s', filtered_text)
        tex_path = render.generate(filtered_text, date=date)
        pdf_path = output.pdftex(tex_path)
        logger.debug('Printing PDF file: %s', pdf_path)
        output.print(pdf_path, qty)
    except output.PrintError as e:
        logger.error('Could not print label: %s', e)
        return False
    else:
        logger.debug('Printed label: %s', filtered_text)
        # TODO: cleanup files
        return True
