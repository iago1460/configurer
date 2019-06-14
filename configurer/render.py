import logging
import os
import shutil
from pathlib import Path
from jinja2 import Template


def replace_file(source_file_path, output_file_path, template_vars):
    try:
        file_data = _render_template_from_file(source_file_path, template_vars)
    except UnicodeDecodeError:
        logging.debug(f"Can't read file {source_file_path}, copying it instead")
        shutil.copy2(source_file_path, output_file_path)
    else:
        with output_file_path.open('w') as file:
            file.write(file_data)
        logging.debug('Copying permissions')
        shutil.copystat(source_file_path, output_file_path)


def render_dir(source_path, output_target_path, get_template_vars_func):
    for root, dirs, files in os.walk(source_path):
        relative_path = Path(root).relative_to(source_path)
        output_path = output_target_path.joinpath(relative_path)
        logging.debug(f'Creating dir "{relative_path}"')
        try:
            os.makedirs(output_path)
        except FileExistsError:
            pass

        for file in files:
            source_file_path = Path(root).joinpath(file)
            output_file_path = output_path.joinpath(file)
            logging.debug(f'Creating file "{output_file_path}"')
            replace_file(
                source_file_path=source_file_path,
                output_file_path=output_file_path,
                template_vars=get_template_vars_func()
            )


def _render_template_from_file(file_path, template_vars):
    with file_path.open('r') as file:
        template = file.read()

    template = Template(template)
    return template.render(**template_vars)
