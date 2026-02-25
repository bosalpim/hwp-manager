"""HWP 바이너리(OLE2) 파일 읽기 - olefile 기반."""
from __future__ import annotations

import struct
import zlib
from typing import List


class HwpReader:
    """HWP(OLE2) 파일에서 문단 텍스트를 추출한다."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def read(self) -> List[str]:
        """파일을 파싱해 문단 텍스트 목록을 반환한다."""
        import olefile

        if not olefile.isOleFile(self.filepath):
            raise ValueError(f"유효한 HWP 파일이 아닙니다: {self.filepath}")

        ole = olefile.OleFileIO(self.filepath)
        try:
            header = ole.openstream("FileHeader").read()
            is_compressed = bool(header[36] & 1)

            paragraphs: List[str] = []
            section_idx = 0
            while True:
                stream_name = f"BodyText/Section{section_idx}"
                if not ole.exists(stream_name):
                    break
                body = ole.openstream(stream_name).read()
                if is_compressed:
                    body = zlib.decompress(body, -15)

                paragraphs.extend(self._parse_section(body))
                section_idx += 1

            return paragraphs
        finally:
            ole.close()

    def _parse_section(self, body: bytes) -> List[str]:
        paragraphs: List[str] = []
        offset = 0
        while offset < len(body) - 4:
            hdr = struct.unpack("<I", body[offset : offset + 4])[0]
            tag = hdr & 0x3FF
            size = (hdr >> 20) & 0xFFF
            if size == 0xFFF:
                if offset + 8 > len(body):
                    break
                size = struct.unpack("<I", body[offset + 4 : offset + 8])[0]
                data_off = offset + 8
            else:
                data_off = offset + 4

            if data_off + size > len(body):
                break

            if tag == 67:  # PARA_TEXT
                text = _decode_hwp_text(body[data_off : data_off + size])
                if text.strip():
                    paragraphs.append(text)

            offset = data_off + size
            if offset <= data_off:
                break

        return paragraphs


def _decode_hwp_text(data: bytes) -> str:
    """HWP UTF-16LE 텍스트 데이터를 디코딩한다 (제어 코드 처리 포함)."""
    decoded = ""
    i = 0
    while i < len(data) - 1:
        cc = struct.unpack("<H", data[i : i + 2])[0]
        if cc == 0:
            break
        elif cc < 32:
            if cc in {1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23}:
                i += 16
                continue
            elif cc == 10:
                decoded += "\n"
            elif cc == 9:
                decoded += "\t"
        elif 0x20 <= cc <= 0xFFFF and not (0xD800 <= cc <= 0xDFFF):
            decoded += chr(cc)
        i += 2
    return decoded.strip()
