# 공유 검사 코드 출처

이 폴더의 `emit.py`, `test_echo_contract.py`, `test_emit.py`는 이한결 님의 10.1절 실습 코드에서 변경 없이 가져왔다.

출처: https://github.com/hanliger/vibecoding/tree/6aaf5ead292200cd84d4da76f7f4e6b350942cfb/ko/examples/10-1-click-3487

원고에 보고된 10.1절 자체 실행과 별도로, 2026-11-24에 Windows 11, Python 3.14.5, pytest 9.2.0, Click `d42f15b` 및 한 줄 패치에서 실행했다. 결과는 `../logs/before-shared-10-1.txt`와 `../logs/after-shared-10-1.txt`에 있다. 검사 12개 중 수정 전 4개 실패와 8개 통과, 수정 후 12개 통과를 확인했다.
