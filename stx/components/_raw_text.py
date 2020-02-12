from __future__ import annotations

import re
from io import StringIO
from typing import List, Iterable, Optional, TextIO

from stx.design.attributes_map import AttributesMap

from stx.utils.strs import crop_text

from ._component import Component
from ..utils.stx_error import StxError


class RawText(Component):

    def __init__(self, text: str):
        self.content = text

    def __repr__(self):
        return f'RawText<{crop_text(self.content, 10)}>'

    def write_text(self, output: TextIO):
        output.write(self.content)

    def get_children(self) -> List[Component]:
        return []
