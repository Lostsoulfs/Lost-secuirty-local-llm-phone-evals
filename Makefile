.PHONY: test proof doctor scan whitespace report-check check clean

PY ?= python

test:
	$(PY) -m pytest

proof:
	$(PY) -m phone_eval_kit proof

doctor:
	$(PY) -m phone_eval_kit doctor

scan:
	$(PY) tools/scan_staged.py

whitespace:
	$(PY) tools/check_whitespace.py

report-check:
	$(PY) tools/generate_report.py --check

check: test proof scan whitespace report-check

clean:
	$(PY) -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"
	$(PY) -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', 'build', 'dist']]"
