# ContactBook 📝
[2025-1] 

## 전화번호부 프로그램

이 프로그램은 GUI 기반의 전화번호부 애플리케이션으로, 연락처 정보를 관리할 수 있습니다.

### 기능

- 연락처 추가: 이름, 전화번호, 그룹 정보를 입력하여 새 연락처 추가
- 연락처 삭제: 선택한 연락처 삭제
- 연락처 수정: 기존 연락처 정보 수정
- 연락처 검색: 키워드로 연락처 검색
- 연락처 목록 출력: 모든 연락처 목록 표시
- 파일 저장: 연락처 정보를 JSON 파일로 저장 및 불러오기
- 테마 변경: 라이트 모드와 다크 모드 전환 기능
- 글꼴 변경: 애플리케이션 글꼴 크기 및 종류 변경 기능
- 컨텍스트 메뉴: 연락처에서 오른쪽 마우스 클릭으로 빠른 작업 수행

### 실행 방법

```bash
python contact_book.py
```

### 사용 방법

1. 프로그램을 실행하면 연락처 목록이 표시됩니다.
2. 상단의 검색창을 사용하여 연락처를 검색할 수 있습니다.
3. '추가' 버튼을 클릭하여 새 연락처를 추가할 수 있습니다.
4. 연락처를 클릭하면 수정 창이 열립니다.
5. 연락처에서 오른쪽 마우스 클릭하면 컨텍스트 메뉴(변경, 출력, 삭제)가 표시됩니다.
6. 상단 메뉴에서 '보기'를 클릭하여 테마(라이트/다크 모드)와 글꼴을 변경할 수 있습니다.

### 파일 구조

- `contact_book.py`: 메인 GUI 애플리케이션
- `contact_manager.py`: 연락처 데이터 관리 클래스
- `contacts.json`: 연락처 데이터가 저장되는 파일 (자동 생성)
- `README.md`: 프로그램 설명 및 사용 방법

### 요구사항

- Python 3.7 이상 (Python 3.13에서 테스트됨)
- Tkinter (Python 표준 라이브러리에 포함)

### 버전 호환성 참고사항

- Python 3.7 ~ 3.12: 코드 내 `trace_add("write", callback)` 부분을 `trace("w", callback)`으로 변경해야 할 수 있습니다.
- Python 3.13 이상: 현재 코드가 그대로 작동합니다.

### 설치 방법

#### macOS
```
brew install python-tk@3.13  # Python 3.13 사용 시
# 또는
brew install python-tk  # 다른 Python 버전 사용 시
```

#### Windows
Windows에서는 대부분의 Python 설치 시 Tkinter가 함께 설치됩니다. 별도 설치가 필요 없습니다.

#### Linux
```
sudo apt-get install python3-tk  # Debian/Ubuntu
# 또는
sudo dnf install python3-tkinter  # Fedora
