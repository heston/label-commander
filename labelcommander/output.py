import logging
import os.path
import re
import subprocess

from . import settings

logger = logging.getLogger(__name__)
output_pattern = re.compile(r'Output written on ([^\s]+\.pdf) \(')
PDFLATEX_COMMAND = 'pdflatex'
PDFLATEX_TIMEOUT = 10
PRINT_COMMAND = 'lp'
PRINT_TIMEOUT = 5
PRINTER_NAME = settings.CUPS_PRINTER_NAME


class PrintError(RuntimeError):
    """Error raised when trying to print."""


def get_output_filename(output_log):
    cleaned_output = str(output_log).replace('\\n', '')
    output_file = output_pattern.search(cleaned_output)
    if not output_file:
        logger.debug(cleaned_output)
        raise PrintError('No suitable output file found!')

    return output_file.group(1)


def pdftex(input_path):
    output_dir = os.path.dirname(input_path)
    args = [PDFLATEX_COMMAND, '-output-directory', output_dir, input_path]

    try:
        completed_process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=PDFLATEX_TIMEOUT
        )
        completed_process.check_returncode()
    except subprocess.CalledProcessError as e:
        logger.debug('%s: %s', e, completed_process.stderr)
        raise PrintError('pdftex failure')
    except subprocess.TimeoutExpired as e:
        raise PrintError(e)

    return get_output_filename(completed_process.stdout)


def print(filepath):
    args = [
        PRINT_COMMAND,
        '-d', PRINTER_NAME,
        # Only print the first page
        '-o', 'page-ranges=1',
        filepath
    ]

    try:
        completed_process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=PRINT_TIMEOUT
        )
        completed_process.check_returncode()
    except subprocess.CalledProcessError as e:
        logger.debug(completed_process.stderr)
        raise PrintError('cups failure')
