from __future__ import annotations

from tools.check_whitespace import ROOT, check_file, main


def test_check_file_detects_extra_blank_eof(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("ok\n\n", encoding="utf-8")
    assert any("extra blank line" in error for error in check_file(path))


def test_check_file_accepts_single_final_newline(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("ok\n", encoding="utf-8")
    assert check_file(path) == []


def test_main_skips_deleted_tracked_files(monkeypatch, capsys):
    missing = ROOT / "definitely-missing-for-whitespace-test.txt"
    monkeypatch.setattr("tools.check_whitespace.tracked_files", lambda: [missing])
    assert main() == 0
    assert "PASS" in capsys.readouterr().out
