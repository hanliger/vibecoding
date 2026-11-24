#!/bin/bash
# 사용법: grade.sh <run 디렉터리>  — 에이전트가 고친 src를 고정된 테스트 사본으로 채점한다.
R=$1; G=$(dirname "$R")/grade; PY="$R/venv/bin/python"
run(){ (cd "$1" && PYTHONDONTWRITEBYTECODE=1 "$PY" -m pytest -q -p no:cacheprovider -o addopts="" "${@:2}" < /dev/null 2>&1 | tail -1); }
echo "A 한결님 검사 12건:      $(run $G/hanliger test_echo_contract.py test_emit.py)"
echo "B 공식 test_utils.py:   $(run $G/official_full/tests test_utils.py)"
echo "C 수정 전 전체 테스트:   $(run $G/pristine/tests . -k "not stress" -x)"
echo "D 에이전트 쪽 tests/:    $(run $R/click/tests . -k "not stress")"
