from pathlib import Path
import subprocess, os, json, sys, hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REPO=HERE/'click'
PY=ROOT/'click-3487/.venv/Scripts/python.exe'
env=dict(os.environ,PYTHONPATH=str(REPO/'src'),PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
LOG=HERE/'logs'
phase=sys.argv[1]
records=[]
def run(label,args,expected=0,stdin=None):
    args=[str(x) for x in args]
    q=subprocess.run(args,cwd=REPO,env=env,input=stdin,text=True,encoding='utf-8',errors='replace',capture_output=True)
    out=q.stdout+q.stderr
    (LOG/f'{label}.txt').write_text(out,encoding='utf-8')
    records.append({'label':label,'argv':args,'stdin':stdin,'exit_code':q.returncode})
    print(label,'exit',q.returncode,'\n',out[-5000:])
    assert q.returncode==expected,(label,q.returncode)
if phase=='reproduce':
    run('environment',[PY,'-c','import sys,click,pytest,platform;print(sys.version);print(platform.platform());print("click source",click.__file__);print("pytest",pytest.__version__)'])
    run('before-repro',[PY,HERE/'repro.py'],1)
    run('before-matrix',[PY,HERE/'matrix.py'])
    run('before-tests',[PY,'-m','pytest',HERE/'test_echo_3487.py','-q','--tb=short'],1)
    run('before-existing',[PY,'-m','pytest','tests/test_utils.py','-q','--tb=short'])
elif phase=='observe':
    src=(REPO/'src/click/utils.py').as_posix()
    commands=f'b {src}:297\nc\np (type(out).__name__, repr(out))\nn\np (type(out).__name__, repr(out))\nq\n'
    run('pdb-observation',[PY,'-m','pdb',HERE/'repro.py'],stdin=commands)
elif phase=='verify':
    run('after-repro',[PY,HERE/'repro.py'])
    run('after-matrix',[PY,HERE/'matrix.py'])
    run('after-tests',[PY,'-m','pytest',HERE/'test_echo_3487.py','-q','--tb=short'])
    run('after-existing',[PY,'-m','pytest','tests/test_utils.py','-q','--tb=short'])
    run('final-diff',['git','diff','--','src/click/utils.py'])
else:
    raise ValueError(phase)
record={'phase':phase,'timestamp_kst':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),'model':'gpt-6-astra (current session identity)','agent':'Codex desktop current assistant, not an independent blind agent run','base_commit':'d42f15b71757de791a5781fb179fd972da9169f5','known_solution':True,'test_sha256':hashlib.sha256((HERE/'test_echo_3487.py').read_bytes()).hexdigest(),'commands':records}
(LOG/f'{phase}-metadata.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
