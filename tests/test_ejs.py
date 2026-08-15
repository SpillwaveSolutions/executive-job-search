#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ejs_common.py"
SESSION = ROOT / "scripts" / "brain_session.py"
SAMPLE = ROOT / "sample-knowledge"


def run(*args, env=None):
    e = os.environ.copy()
    if env:
        e.update(env)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        env=e,
    )


def run_session(*args):
    return subprocess.run(
        [sys.executable, str(SESSION), *args],
        capture_output=True,
        text=True,
    )


def git(cwd, *args):
    return subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        check=True,
    )


def test_sample_validates():
    r = run("validate", "--bundle", str(SAMPLE))
    assert r.returncode == 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    assert data["ok"] is True
    assert data["concepts"] >= 1


def test_write_requires_author():
    with tempfile.TemporaryDirectory() as td:
        bundle = Path(td) / "knowledge"
        run("init-bundle", "--bundle", str(bundle), "--title", "Test", "--catalogs", "job-leads")
        r = run(
            "write",
            "--bundle",
            str(bundle),
            "--type",
            "JobLead",
            "--folder",
            "job-leads",
            "--title",
            "No Author",
        )
        assert r.returncode != 0
        assert "identity" in r.stdout.lower() or "identity" in r.stderr.lower()


def test_init_and_write():
    with tempfile.TemporaryDirectory() as td:
        bundle = Path(td) / "knowledge"
        r = run("init-bundle", "--bundle", str(bundle), "--title", "Test", "--catalogs", "job-leads")
        assert r.returncode == 0, r.stdout + r.stderr
        r = run(
            "write",
            "--bundle",
            str(bundle),
            "--type",
            "JobLead",
            "--folder",
            "job-leads",
            "--title",
            "Hello World",
            "--author",
            "grok-bot/executive-job-search",
        )
        assert r.returncode == 0, r.stdout + r.stderr
        data = json.loads(r.stdout)
        assert data["author"] == "grok-bot/executive-job-search"
        assert data["event"]
        r = run("validate", "--bundle", str(bundle))
        assert r.returncode == 0, r.stdout + r.stderr


def test_isolation_two_sessions_do_not_clobber():
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td) / "brain"
        repo.mkdir()
        git(repo, "init", "-b", "main")
        git(repo, "config", "user.email", "test@example.com")
        git(repo, "config", "user.name", "tester")
        knowledge = repo / "knowledge"
        r = run("init-bundle", "--bundle", str(knowledge), "--title", "Shared", "--catalogs", "job-leads")
        assert r.returncode == 0, r.stdout + r.stderr
        git(repo, "add", ".")
        git(repo, "commit", "-m", "seed")

        a = run_session(
            "open",
            "--repo",
            str(repo),
            "--bundle",
            "knowledge",
            "--actor",
            "claude-code/threatiq",
            "--host",
            "claude-code",
            "--plugin",
            "executive-job-search",
        )
        assert a.returncode == 0, a.stdout + a.stderr
        sa = json.loads(a.stdout)
        b = run_session(
            "open",
            "--repo",
            str(repo),
            "--bundle",
            "knowledge",
            "--actor",
            "deep-agents/executive-job-search",
            "--host",
            "deep-agents",
            "--plugin",
            "executive-job-search",
        )
        assert b.returncode == 0, b.stdout + b.stderr
        sb = json.loads(b.stdout)
        assert sa["branch"] != sb["branch"]
        assert sa["worktree"] != sb["worktree"]

        r = run(
            "write",
            "--bundle",
            sa["bundle"],
            "--type",
            "JobLead",
            "--folder",
            "job-leads",
            "--title",
            "Session A Note",
            "--author",
            "claude-code/threatiq",
        )
        assert r.returncode == 0, r.stdout + r.stderr
        r = run(
            "write",
            "--bundle",
            sb["bundle"],
            "--type",
            "JobLead",
            "--folder",
            "job-leads",
            "--title",
            "Session B Note",
            "--author",
            "deep-agents/executive-job-search",
        )
        assert r.returncode == 0, r.stdout + r.stderr

        assert (Path(sa["bundle"]) / "job-leads" / "session-a-note.md").exists()
        assert not (Path(sa["bundle"]) / "job-leads" / "session-b-note.md").exists()
        assert (Path(sb["bundle"]) / "job-leads" / "session-b-note.md").exists()
        assert not (Path(sb["bundle"]) / "job-leads" / "session-a-note.md").exists()

        ca = run_session("close", "--repo", str(repo), "--session", sa["session_id"], "--no-push", "--allow-local")
        assert ca.returncode == 0, ca.stdout + ca.stderr
        cb = run_session("close", "--repo", str(repo), "--session", sb["session_id"], "--no-push", "--allow-local")
        assert cb.returncode == 0, cb.stdout + cb.stderr

        git(repo, "merge", "--no-ff", sa["branch"], "-m", "merge a")
        git(repo, "merge", "--no-ff", sb["branch"], "-m", "merge b")
        assert (knowledge / "job-leads" / "session-a-note.md").exists()
        assert (knowledge / "job-leads" / "session-b-note.md").exists()


if __name__ == "__main__":
    test_sample_validates()
    test_write_requires_author()
    test_init_and_write()
    test_isolation_two_sessions_do_not_clobber()
    print("ok")
