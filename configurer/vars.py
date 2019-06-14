import os


def get_vars(file):
    return {**_get_vars_from_env(), **_get_vars_from_file(file)}


def _get_vars_from_env():
    return dict(os.environ)


def _get_vars_from_file(file_path):
    file_vars = {}
    if file_path:
        with file_path.open('r') as file:
            for line in file.readlines():
                # TODO: replace with regex
                line_split = line.strip().split('=')
                if line_split[0] != '#' and len(line_split) > 1:
                    var_name = line_split[0].replace('export ', '').strip()
                    var_data = ''.join(line_split[1:])
                    file_vars[var_name] = var_data
    return file_vars
