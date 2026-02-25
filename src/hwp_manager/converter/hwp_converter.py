"""HWP 파싱 결과를 텍스트로 변환한다."""
from __future__ import annotations

from typing import List


class HwpConverter:
    """HwpReader.read() 결과를 받아 포맷으로 변환한다."""

    def __init__(self, paragraphs: List[str]) -> None:
        self.paragraphs = paragraphs

    def to_txt(self) -> str:
        """문단 목록을 줄바꿈으로 이어 plain text로 반환한다."""
        return "\n".join(self.paragraphs)
