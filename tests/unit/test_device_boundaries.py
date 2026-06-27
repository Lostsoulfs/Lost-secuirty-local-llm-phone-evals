from __future__ import annotations

from phone_eval_kit.device.adb import snapshot_device


def test_device_snapshot_requires_opt_in(monkeypatch):
    monkeypatch.delenv("PHONE_EVALS_DEVICE", raising=False)
    snapshot = snapshot_device()
    assert snapshot["status"] == "skipped"
