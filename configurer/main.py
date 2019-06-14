import argparse
import logging
import sys
import time
from argparse import RawTextHelpFormatter

from pathlib import Path

from .render import render_dir
from .vars import get_vars
from .watcher import Watcher, EnvEventHandler, FilesEventHandler

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def PathType(path):
    if path:
        return Path(path).resolve(strict=True)
    return None


def main():
    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description=
        "Renders files replacing variables when possible.\n"
        "Example usage:\n"
        "python3 -m configurer --source ./demo/config_templates --output ./config"
    )
    parser.add_argument(
        "--vars",
        help=f"Path to the file with variables.",
        dest='vars_path',
        type=PathType,
        default=None
    )
    parser.add_argument(
        '--output',
        help=f"Path to the output directory.",
        dest='output_path',
        type=PathType,
        required=True,
    )
    parser.add_argument(
        '--source',
        help=f"Path to the source directory.",
        dest='source_path',
        type=PathType,
        required=True,
    )
    parser.add_argument(
        '--watch',
        help=f"Keep watching for changes.",
        dest='watch',
        action='store_true',
        default=False
    )

    args = parser.parse_args()

    def get_template_vars_func():
        return get_vars(file=args.vars_path)

    render_dir(args.source_path, args.output_path, get_template_vars_func)

    if args.watch:
        watchers = [
            Watcher(
                args.source_path,
                FilesEventHandler(get_template_vars_func, args.source_path, args.output_path),
                True
            )
        ]
        if args.vars_path:
            watchers.append(
                Watcher(
                    args.vars_path.parent,
                    EnvEventHandler(get_template_vars_func, args.source_path, args.output_path),
                    False
                )
            )
        for watch in watchers:
            watch.run()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for watch in watchers:
                watch.stop()


if __name__ == '__main__':
    main()
