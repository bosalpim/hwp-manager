"""HWPX 파싱 결과를 Markdown 또는 plain text로 변환한다."""
from __future__ import annotations

import re
from typing import List, Tuple, Union

from lxml import etree

from hwp_manager.reader.hwpx_reader import NS, get_cell_text

Item = Tuple[str, Union[str, etree._Element]]


class HwpxConverter:
    """HwpxReader.read() 결과를 받아 포맷으로 변환한다."""

    def __init__(self, items: List[Item]) -> None:
        self.items = items

    def to_md(self) -> str:
        """아이템 목록을 Markdown으로 변환한다."""
        md: List[str] = []
        for kind, content in self.items:
            if kind == "tbl":
                md.append("\n" + _tbl_to_md(content))
            else:
                line = content
                if re.match(r"^\d+\.\s+\S", line) and not re.match(r"^\d{4}\.\s", line):
                    md.append(f"\n## {line}")
                elif re.match(r"^[가-하]\.\s", line):
                    md.append(f"\n### {line}")
                elif re.match(r"^[-◦]\s", line):
                    md.append(f"- {line[2:].strip()}")
                elif re.match(r"^\d+\)\s", line):
                    md.append(f"- {line}")
                elif re.match(r"^\d{4}\.\s", line):
                    md.append(f"\n> {line}")
                else:
                    md.append(line)
        return "\n".join(md)

    def to_txt(self) -> str:
        """아이템 목록을 plain text로 변환한다 (테이블 셀은 탭으로 구분)."""
        lines: List[str] = []
        for kind, content in self.items:
            if kind == "tbl":
                rows = content.findall(".//hp:tr", NS)
                for row in rows:
                    cells = row.findall("hp:tc", NS)
                    lines.append("\t".join(get_cell_text(c) for c in cells))
            else:
                lines.append(content)
        return "\n".join(lines)


def _tbl_to_md(tbl: etree._Element) -> str:
    """hp:tbl 엘리먼트를 Markdown 테이블 문자열로 변환한다."""
    rows = tbl.findall(".//hp:tr", NS)
    if not rows:
        return ""

    md_rows = []
    for row in rows:
        cells = row.findall("hp:tc", NS)
        md_rows.append([get_cell_text(c) for c in cells])

    if not md_rows:
        return ""

    max_cols = max(len(r) for r in md_rows)
    for r in md_rows:
        while len(r) < max_cols:
            r.append("")

    lines = [
        "| " + " | ".join(md_rows[0]) + " |",
        "| " + " | ".join(["---"] * max_cols) + " |",
    ]
    for row in md_rows[1:]:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)
