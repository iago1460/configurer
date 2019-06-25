import logging
import os
import shutil
from functools import wraps

from pathlib import Path
from .render import replace_file, render_dir
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def ignore_errors(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
    return wrapped


class FilesEventHandler(FileSystemEventHandler):

    def __init__(self, get_template_vars_func, source_path, output_path, *args, **kwargs):
        self.get_template_vars_func = get_template_vars_func
        self.source_path = source_path
        self.output_path = output_path
        super(FilesEventHandler, self).__init__(*args, **kwargs)

    @ignore_errors
    def on_created(self, event):
        logging.debug('create event')
        self._render(event)

    @ignore_errors
    def on_modified(self, event):
        logging.debug('modified event')
        self._render(event)

    def _render(self, event):
        path = Path(event.src_path)
        dir_folder = path

        if not event.is_directory:
            dir_folder = path.parent
        try:
            os.makedirs(dir_folder)
        except FileExistsError:
            pass

        if not event.is_directory:
            output_file_path = self._get_target_path(path)
            logging.debug(f'rendering {output_file_path}')
            replace_file(
                source_file_path=path,
                output_file_path=output_file_path,
                template_vars=self.get_template_vars_func()
            )
            logging.info(f'File "{output_file_path}" was processed')

    def _get_target_path(self, path):
        relative_path = Path(path).relative_to(self.source_path)
        return self.output_path.joinpath(relative_path)

    @ignore_errors
    def on_deleted(self, event):
        logging.debug('deleted event')
        output_path = self._get_target_path(event.src_path)
        if output_path.is_dir():
            shutil.rmtree(output_path)
        else:
            output_path.unlink()


class EnvEventHandler(FileSystemEventHandler):

    def __init__(self, get_template_vars_func, source_path, output_path, *args, **kwargs):
        self.get_template_vars_func = get_template_vars_func
        self.source_path = source_path
        self.output_path = output_path
        super(EnvEventHandler, self).__init__(*args, **kwargs)

    @ignore_errors
    def on_created(self, event):
        logging.debug('env create event')
        self._render(event)

    @ignore_errors
    def on_modified(self, event):
        logging.debug('env modified event')
        self._render(event)

    def _render(self, event):
        render_dir(self.source_path, self.output_path, self.get_template_vars_func)
        logging.info(f'Config was processed')


class Watcher:

    def __init__(self, src_path, event_handler, recursive):
        self.__recursive = recursive
        self.__src_path = str(src_path)
        self.__event_handler = event_handler
        self.__event_observer = Observer()

    def run(self):
        self.start()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=self.__recursive
        )