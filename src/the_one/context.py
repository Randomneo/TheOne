from typing import Optional


class Context:
    def __init__(self):
        self._cur_line = 0
        self._next_line_indent = 0
        self._cur_line_indent = 0
        self._context = []

    def indent_line(self, line: str) -> tuple[str, Optional[str]]:
        indent = ' '*4*self._cur_line_indent
        self._cur_line_indent = self._next_line_indent
        self._cur_line += 1
        return f'{indent}{line.strip()}', None
