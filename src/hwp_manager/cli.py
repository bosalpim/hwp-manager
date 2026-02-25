"""hwm CLI - HWP/HWPX 파일 변환 커맨드라인 도구."""
from __future__ import annotations

import argparse
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="hwm",
        description="HWP/HWPX 파일을 다른 포맷으로 변환합니다.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert_parser = subparsers.add_parser("convert", help="파일을 변환합니다.")
    convert_parser.add_argument("file", help="변환할 HWP 또는 HWPX 파일 경로")
    convert_parser.add_argument(
        "--to",
        required=True,
        choices=["txt", "md"],
        help="출력 포맷 (txt: plain text, md: Markdown)",
    )
    convert_parser.add_argument(
        "-o", "--output",
        help="출력 파일 경로 (생략 시 stdout으로 출력)",
    )

    args = parser.parse_args()

    if args.command == "convert":
        _run_convert(args)


def _run_convert(args: argparse.Namespace) -> None:
    filepath: str = args.file
    fmt: str = args.to

    if not os.path.exists(filepath):
        print(f"오류: 파일을 찾을 수 없습니다: {filepath}", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(filepath)[1].lower()

    try:
        content = _convert(filepath, ext, fmt)
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"저장 완료: {args.output}", file=sys.stderr)
    else:
        print(content)


def _convert(filepath: str, ext: str, fmt: str) -> str:
    if ext == ".hwp":
        if fmt == "txt":
            from hwp_manager import hwp_to_txt
            return hwp_to_txt(filepath)
        raise ValueError(f"HWP 파일은 txt 포맷만 지원합니다. (요청: {fmt})")

    if ext == ".hwpx":
        if fmt == "md":
            from hwp_manager import hwpx_to_md
            return hwpx_to_md(filepath)
        if fmt == "txt":
            from hwp_manager import hwpx_to_txt
            return hwpx_to_txt(filepath)

    raise ValueError(f"지원하지 않는 파일 형식입니다: {ext}")


if __name__ == "__main__":
    main()
