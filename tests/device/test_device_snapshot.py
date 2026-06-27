from __future__ import annotations

import os

import pytest

from phone_eval_kit.device.adb import snapshot_device

pytestmark = [
    pytest.mark.device,
    pytest.mark.skipif(
        os.environ.get("PHONE_EVALS_DEVICE") != "1",
        reason="PHONE_EVALS_DEVICE=1 is required for real device tests",
    ),
]

def test_real_device_snapshot_when_enabled():
    snapshot = snapshot_device()
    assert snapshot["status"] == "collected"
    assert "serial_sha256_16" in snapshot
