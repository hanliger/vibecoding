# 고전적 IDE 디버거 화면

촬영일: 2026-11-25, 한국 표준시.

원고에 넣은 두 그림은 Python 기본 IDE인 IDLE의 Debug Control 창을 실제로 실행해 촬영했다. 화면의 변수 값이나 코드 위치를 다시 그리거나 합성하지 않았다.

| 항목 | 촬영 조건 |
| --- | --- |
| IDE와 인터프리터 | Python IDLE 3.12.10 / CPython 3.12.10 |
| 운영체제 | Windows 11 |
| Click 소스 | `d42f15b71757de791a5781fb179fd972da9169f5` |
| 실행 코드 | 이 폴더의 `repro.py` |
| 중단점 | `src/click/utils.py`의 297행 |
| 첫 화면 | 해당 줄 실행 전, `out`은 `b''` |
| 두 번째 화면 | Over로 한 줄 실행 후 298행, `out`은 `''` |

그림 파일은 책의 `ko/images/10-2-debugging/idle-before.jpg`와 `idle-after.jpg`다. `screenshot-metadata.json`에 파일 해시와 소스의 LF 기준 해시를 적었다. Windows의 CRLF 줄바꿈을 LF로 정규화하면 소스는 지정한 커밋의 원본과 일치한다.

## 같은 상태 확인하기

1. 기준 커밋의 Click 소스를 사용하는 환경에서 IDLE로 `repro.py`를 연다. 설치된 다른 Click 복사본 대신 지정한 소스를 사용해야 한다.
2. IDLE Shell의 Debug 메뉴에서 Debugger를 켠다.
3. 같은 IDLE 세션에서 `src/click/utils.py`를 열고 Alt+G의 Go To Line에 297을 입력한다.
4. 그 줄에서 마우스 오른쪽 메뉴의 Set Breakpoint를 선택한다.
5. `repro.py`를 실행하고 Debug Control의 Go로 중단점까지 진행한다.
6. Stack에 297행, Locals에 `message b''`, `nl True`, `out b''`가 보이는지 확인한다.
7. Over를 한 번 누른다. 현재 위치는 298행이 되고 `message`는 그대로지만 `out`은 `''`가 된다.

촬영 때는 이미 오류가 해결된 로컬 설치본과 혼동하지 않도록 기준 커밋의 별도 소스 복사본을 `PYTHONPATH`로 지정했다. IDE 화면용 실행은 2026-11-24에 CPython 3.14.5에서 수행한 검사와 별개다. 기존 검사 횟수나 통과 수를 추가한 것으로 계산하지 않는다.

출처: [Python Software Foundation, IDLE: Python editor and shell](https://docs.python.org/3.12/library/idle.html#debug-menu-shell-window-only), Debug menu와 Context menus (확인: 2026-11-25).
