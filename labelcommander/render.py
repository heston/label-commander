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


def render(body, template=None):
    template_name = template or DEFAULT_TEMPLATE_NAME
    template = jinja_env.get_template(template_name)
    return template.render(
        image_path='{}/'.format(IMAGE_PATH),
        body=body
    )


def generate(body):
    fd_handle, temp_path = get_temp_file()
    content = render(body)
    with open(fd_handle, mode='w') as f:
        f.write(content)

    return temp_path
