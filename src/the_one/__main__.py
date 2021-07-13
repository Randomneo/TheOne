"""
Main module
"""


import argparse
import sys
from argparse import Namespace
from typing import Any
from typing import Optional

from context import Context
from processor_manager import ProcessorManager


def get_args(argv: tuple[str]) -> Namespace:
    parser = argparse.ArgumentParser(
        description='',
    )
    parser.add_argument(
        'files',
        type=str,
        nargs='+',
        help='Files to indent',
    )

    return parser.parse_args(argv)


def iterate_lines(file_body: str) -> str:
    processor_manager = ProcessorManager()
    context = Context()
    new_body = []
    for line in file_body.split('\n'):
        context, new_lines = processor_manager.process_all(context, line)
        new_body.extend(new_lines)
    return '\n'.join(new_body)


def main(args: Optional[tuple[Any]] = sys.argv, extra_args: Optional[tuple[Any]] = ()) -> None:
    """
    main entry point
    """
    args = get_args((*args, *extra_args)[1:])
    for file_name in args.files:
        with open(file_name, 'r') as f:
            print(iterate_lines(f.read()))


if __name__ == '__main__':
    sys.exit(main())


__all__ = [
    main.__name__,
]
