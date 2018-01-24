import logging
import os.path
import re
import subprocess

logger = logging.getLogger(__name__)
output_pattern = re.compile(r'Output written on ([^\s]+\.pdf) \(')
PDFLATEX_COMMAND = 'pdflatex'
PRINT_COMMAND = 'lp'
PRINTER_NAME = 'DYMO_LabelWriter_330'


def get_output_filename(output_log):
    cleaned_output = str(output_log).replace('\\n', '')
    output_file = output_pattern.search(cleaned_output)
    if not output_file:
        logger.debug(cleaned_output)
        raise ValueError('No suitable output file found!')

    return output_file.group(1)


def pdftex(input_path):
    output_dir = os.path.dirname(input_path)
    args = [PDFLATEX_COMMAND, '-output-directory', output_dir, input_path]
    completed_process = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        completed_process.check_returncode()
    except subprocess.CalledProcessError as e:
        logger.debug(completed_process.stderr)
        return

    return get_output_filename(completed_process.stdout)


def print(filepath):
    args = [
        PRINT_COMMAND,
        '-d', PRINTER_NAME,
        # '-o', 'landscape',
        # '-o', 'page-ranges=1',
        filepath
    ]
    completed_process = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        completed_process.check_returncode()
    except subprocess.CalledProcessError as e:
        logger.debug(completed_process.stderr)
        return
