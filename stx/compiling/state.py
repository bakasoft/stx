from typing import Optional, List

from stx.compiling.raw_text import compile_lines
from stx.components.content import CContent, CFigure, CTable


class State:

    def __init__(self):
        self.contents: List[Optional[CContent]] = []
        self.attributes: Optional[dict] = None
        self.pending_caption: Optional[CContent] = None
        self.pending_lines: Optional[List[str]] = None

    def push(self, content: CContent):
        self.flush_lines()

        if self.pending_caption is not None:
            if isinstance(content, CTable):
                content.caption = self.pending_caption
            else:
                content = CFigure(content, self.pending_caption)

            self.pending_caption = None

        if self.attributes is not None:
            content.attributes = self.attributes

            self.attributes = None

        self.contents.append(content)

    def push_line(self, line):
        if self.pending_lines is None:
            self.pending_lines = []

        self.pending_lines.append(line)

    def flush_lines(self):
        if self.pending_lines is not None:
            content = compile_lines(self.pending_lines)

            self.pending_lines = None

            if content is not None:
                self.push(content)

    def pop(self) -> CContent:
        if len(self.contents) == 0:
            raise Exception('Expected content')

        return self.contents.pop()

    def compile(self) -> List[CContent]:
        self.flush_lines()

        if self.pending_caption is not None:
            raise Exception('pending cation')

        return [c for c in self.contents if c is not None]

    @property
    def last_content(self) -> Optional[CContent]:
        if len(self.contents) == 0:
            return None

        return self.contents[-1]

    def push_separator(self):
        self.contents.append(None)

    def push_attribute(self, name: str, values: list):
        if self.attributes is None:
            self.attributes = {}

        if name not in self.attributes.keys():
            self.attributes[name] = list()

        self.attributes[name].extend(values)
