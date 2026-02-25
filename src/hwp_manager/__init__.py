"""hwp-manager: HWP/HWPX 파일 읽기 및 변환 라이브러리."""
from .reader.hwp_reader import HwpReader
from .reader.hwpx_reader import HwpxReader
from .converter.hwp_converter import HwpConverter
from .converter.hwpx_converter import HwpxConverter

__all__ = [
    "HwpReader",
    "HwpxReader",
    "HwpConverter",
    "HwpxConverter",
    "hwp_to_txt",
    "hwpx_to_md",
    "hwpx_to_txt",
]


def hwp_to_txt(filepath: str) -> str:
    """HWP 파일을 plain text로 변환해 반환한다."""
    paragraphs = HwpReader(filepath).read()
    return HwpConverter(paragraphs).to_txt()


def hwpx_to_md(filepath: str) -> str:
    """HWPX 파일을 Markdown으로 변환해 반환한다."""
    items = HwpxReader(filepath).read()
    return HwpxConverter(items).to_md()


def hwpx_to_txt(filepath: str) -> str:
    """HWPX 파일을 plain text로 변환해 반환한다."""
    items = HwpxReader(filepath).read()
    return HwpxConverter(items).to_txt()
