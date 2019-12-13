import string
from typing import Dict, Optional, List

from stx.components.content import CContent


def make_ref(base: str, length_hint=40) -> str:
    result = []

    for c in base.lower():
        if c in string.ascii_lowercase or c in string.digits:
            result.append(c)
        elif len(result) >= length_hint:
            break
        elif len(result) == 0 or result[-1] != '-':
            result.append('-')

    return ''.join(result)


def compute_ref(content: CContent, count: Optional[int]) -> str:
    plain_text = ' '.join(content.get_plain_text()).strip()

    if count is not None:
        plain_text += f'-{count}'

    return make_ref(plain_text)


class LinkMap:

    def __init__(self):
        self._ref_cons: Dict[str, CContent] = {}
        self._con_refs: Dict[CContent, List[str]] = {}

    def contains_ref(self, ref: str):
        return ref in self._ref_cons.keys()

    def register_content(self, content: CContent, main=False) -> str:
        count = 0

        while True:
            ref = compute_ref(content, count if count > 0 else None)

            if not self.contains_ref(ref):
                break

            count += 1

        self.register_ref(ref, content, main)

        return ref

    def register_ref(self, ref: str, content: CContent, main=False):
        if self.contains_ref(ref):
            raise Exception(f'Link already registered: {ref}')

        self._ref_cons[ref] = content

        if self._con_refs.get(content, None) is None:
            self._con_refs[content] = []

        if ref not in self._con_refs[content]:
            if main:
                self._con_refs[content].insert(0, ref)
            else:
                self._con_refs[content].append(ref)

    def get_refs(self, content: CContent) -> List[str]:
        return self._con_refs.get(content, [])

    def get_main_ref(self, content: CContent) -> Optional[str]:
        refs = self.get_refs(content)

        if len(refs) == 0:
            return None

        return refs[0]

    def get_other_refs(self, content: CContent) -> List[str]:
        refs = self.get_refs(content)

        if len(refs) <= 1:
            return []

        return refs[1:]

    def get_content(self, ref: str) -> Optional[CContent]:
        return self._ref_cons.get(ref, None)
