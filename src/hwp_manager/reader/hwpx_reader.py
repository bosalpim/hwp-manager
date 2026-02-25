"""HWPX 파일 읽기 - zipfile + lxml 기반."""
from __future__ import annotations

import zipfile
from typing import List, Tuple, Union
from lxml import etree


NS = {
    "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    "hs": "http://www.hancom.co.kr/hwpml/2011/section",
}

# (kind, content) where kind is 'p' or 'tbl'
Item = Tuple[str, Union[str, etree._Element]]


class HwpxReader:
    """HWPX 파일에서 문단과 테이블을 순서대로 추출한다."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def read(self) -> List[Item]:
        """파일을 파싱해 ('p', text) | ('tbl', element) 목록을 반환한다."""
        with zipfile.ZipFile(self.filepath) as z:
            with z.open("Contents/section0.xml") as f:
                tree = etree.parse(f)

        root = tree.getroot()
        items: List[Item] = []

        for child in root.iter():
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag

            if tag == "p":
                ancestor_tags = [p.tag.split("}")[-1] for p in child.iterancestors()]
                if "tbl" in ancestor_tags:
                    continue
                texts = child.findall(".//hp:t", NS)
                text = "".join(t.text or "" for t in texts).strip()
                if text:
                    items.append(("p", text))

            elif tag == "tbl":
                ancestor_tags = [p.tag.split("}")[-1] for p in child.iterancestors()]
                if "tbl" not in ancestor_tags:
                    items.append(("tbl", child))

        return items


def get_cell_text(tc: etree._Element) -> str:
    """테이블 셀(hp:tc) 안의 텍스트를 추출한다."""
    texts = tc.findall(".//hp:t", NS)
    return " ".join(t.text.strip() for t in texts if t.text and t.text.strip())
