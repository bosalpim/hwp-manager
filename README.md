# hwp-manager

HWP/HWPX 파일을 읽고 변환하는 Python 라이브러리입니다.

| 입력 | 출력 | 방법 |
|------|------|------|
| `.hwp` | plain text (`.txt`) | OLE2 바이너리 파싱 (olefile) |
| `.hwpx` | Markdown (`.md`) | ZIP + XML 파싱 (lxml) |
| `.hwpx` | plain text (`.txt`) | ZIP + XML 파싱 (lxml) |

## 설치

> **주의:** 시스템 전역 Python에 설치하면 Python 3.11+ 환경에서 오류가 발생할 수 있습니다. 가상환경 사용을 권장합니다.

### uv 사용 (권장)

```bash
uv venv              # .venv 생성
uv pip install -e .  # 패키지 설치 (olefile, lxml 자동 설치)
```

```bash
# 가상환경 활성화 없이 바로 실행
uv run hwm convert 문서.hwp --to txt

# 또는 가상환경 활성화 후 실행
source .venv/bin/activate
hwm convert 문서.hwp --to txt
```

### venv 사용

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

### 다른 프로젝트에서 import 시

해당 프로젝트의 가상환경에 설치합니다.

```bash
# 로컬 경로
pip install /path/to/hwp-manager

# Git 저장소
pip install git+https://github.com/your-org/hwp-manager
```

## CLI 사용법

설치 후 `hwm` 명령어를 사용할 수 있습니다.

```bash
# HWP → txt (stdout 출력)
hwm convert 문서.hwp --to txt

# HWP → txt (파일로 저장)
hwm convert 문서.hwp --to txt -o 결과.txt

# HWPX → Markdown (stdout 출력)
hwm convert 문서.hwpx --to md

# HWPX → Markdown (파일로 저장)
hwm convert 문서.hwpx --to md -o 결과.md

# HWPX → txt
hwm convert 문서.hwpx --to txt -o 결과.txt
```

## 라이브러리로 사용

### 편의 함수 (고수준 API)

```python
from hwp_manager import hwp_to_txt, hwpx_to_md, hwpx_to_txt

# HWP → txt
text = hwp_to_txt("문서.hwp")

# HWPX → Markdown
md = hwpx_to_md("문서.hwpx")

# HWPX → txt
text = hwpx_to_txt("문서.hwpx")
```

### Reader / Converter 분리 사용 (저수준 API)

읽기와 변환을 단계적으로 제어할 수 있습니다.

```python
from hwp_manager import HwpReader, HwpConverter
from hwp_manager import HwpxReader, HwpxConverter

# HWP 읽기 → txt 변환
paragraphs = HwpReader("문서.hwp").read()   # List[str]
text = HwpConverter(paragraphs).to_txt()

# HWPX 읽기 → md / txt 변환
items = HwpxReader("문서.hwpx").read()      # List[('p'|'tbl', ...)]
md   = HwpxConverter(items).to_md()
text = HwpxConverter(items).to_txt()
```

## 프로젝트 구조

```
src/
  hwp_manager/
    __init__.py          # 공개 API
    cli.py               # CLI (hwm 명령어)
    reader/
      hwp_reader.py      # HWP OLE2 파싱 (olefile)
      hwpx_reader.py     # HWPX ZIP+XML 파싱 (lxml)
    converter/
      hwp_converter.py   # 파싱 결과 → txt
      hwpx_converter.py  # 파싱 결과 → md / txt
pyproject.toml
```
