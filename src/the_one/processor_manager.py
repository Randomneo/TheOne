import re
from itertools import chain
from typing import Optional
from typing import Type

from context import Context


class BaseProcessor:
    def process(self, context: Context, line: str) -> tuple[Context, str]:
        raise NotImplementedError(f'Your class {self.__class__.__name__} mast redefine "process" function')


class IdentProcssor(BaseProcessor):
    def __init__(self):
        self.muliline_def_pattern = re.compile(r'^\t*.*def.*\((?!.*\)).*$')
        self.oneline_def_pattern = re.compile(r'^\t*.*def.*\(.*\).*$')
        self.up_indent_patters = [
            (self.muliline_def_pattern, 2),
            (self.oneline_def_pattern, 1),
        ]

    def process(self, context: Context, line: str) -> tuple[Context, str, Optional[str]]:
        for pattern, up_indent in self.up_indent_patters:
            if pattern.match(line):
                context._next_line_indent += up_indent

        line, sub_line = context.indent_line(line)
        return context, line, sub_line


class ProcessorManager:
    processors_modules = [
        IdentProcssor
    ]

    def __init__(self, additional_processors: Optional[list[Type[BaseProcessor]]] = None):
        self._processors = []
        for processor in chain(self.processors_modules, additional_processors or []):
            if not issubclass(processor, BaseProcessor):
                raise TypeError(f"Passed {processor.__name__} which is not a BaseProcessor")

            self._processors.append(processor())

    def process_all(self, context: Context, line: str) -> tuple[Context, str]:
        new_lines = []
        for processor in self._processors:
            sub_line = True
            while sub_line is not None:
                context, line, sub_line = processor.process(context, line)
                if line is not None:
                    new_lines.append(line)
                line = sub_line

        return context, new_lines
