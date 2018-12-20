from datetime import datetime
import os.path
import tempfile

from jinja2 import Environment, FileSystemLoader, select_autoescape


TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'templates'
)

IMAGE_PATH = os.path.join(
    TEMPLATE_PATH,
    'images'
)

DEFAULT_TEMPLATE_NAME = 'label.tex'

# https://tex.stackexchange.com/a/34586
SPECIAL_TEX_CHARS = {
    '&': '\\&',
    '%': '\\%',
    '$': '\\$',
    '#': '\\#',
    '_': '\\_',
    '{': '\\{',
    '}': '\\}',
}

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_PATH),
    autoescape=select_autoescape(disabled_extensions=('tex',)),
    block_start_string='<!',
    block_end_string='!>',
    variable_start_string='<<',
    variable_end_string='>>'
)


def get_temp_file():
    return tempfile.mkstemp(suffix='.tex', text=True)


def format_date(ts=None):
    if ts is None:
        dt = datetime.now()
    else:
        try:
            dt = datetime.fromtimestamp(ts)
        except (ValueError, OverflowError):
            # Assume ts was microseconds. Convert to seconds.
            dt = datetime.fromtimestamp(ts/1000)

    return f'{dt:%B} {dt.day}, {dt.year}'


def escape_for_tex(body):
    for (search_char, replace_seq) in SPECIAL_TEX_CHARS.items():
        body = body.replace(search_char, replace_seq)
    return body


def render(body, **kwargs):
    escaped_body = escape_for_tex(body)
    date = format_date(kwargs.get('date'))
    template_name = kwargs.get('template') or DEFAULT_TEMPLATE_NAME
    template = jinja_env.get_template(template_name)
    return template.render(
        image_path='{}/'.format(IMAGE_PATH),
        body=escaped_body,
        date=date
    )


def generate(body, **kwargs):
    fd_handle, temp_path = get_temp_file()
    content = render(body, **kwargs)
    with open(fd_handle, mode='w') as f:
        f.write(content)

    return temp_path
