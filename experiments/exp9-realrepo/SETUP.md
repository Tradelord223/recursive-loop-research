# Exp9 setup (reproduce)
git clone https://github.com/python-semver/python-semver semver-src
python3 -m venv .venv && .venv/bin/pip install pytest pytest-cov && .venv/bin/pip install -e ./semver-src
# then, per real bugfix commit:
./run_task.sh <commit> src/semver/version.py "<bug description (no fix leak)>"
# tasks run this session: bc41390 (FAIL), 4b03f86 (PASS), d8813b6 (FAIL). See results.md.
