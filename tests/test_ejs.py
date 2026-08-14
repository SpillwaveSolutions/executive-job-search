#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ejs_common.py"
SAMPLE = ROOT / "sample-knowledge"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def test_sample_validates():
    r = run("validate", "--bundle", str(SAMPLE))
    assert r.returncode == 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    assert data["ok"] is True
    assert data["concepts"] >= 1


def test_init_and_write():
    with tempfile.TemporaryDirectory() as td:
        bundle = Path(td) / "knowledge"
        r = run("init-bundle", "--bundle", str(bundle), "--title", "Test", "--catalogs", "job-leads")
        assert r.returncode == 0, r.stdout + r.stderr
        r = run(
            "write",
            "--bundle", str(bundle),
            "--type", "JobLead",
            "--folder", "job-leads",
            "--title", "Hello World",
            "--author", "Grok Bot: Test",
        )
        assert r.returncode == 0, r.stdout + r.stderr
        r = run("validate", "--bundle", str(bundle))
        assert r.returncode == 0, r.stdout + r.stderr


if __name__ == "__main__":
    test_sample_validates()
    test_init_and_write()
    print("ok")
