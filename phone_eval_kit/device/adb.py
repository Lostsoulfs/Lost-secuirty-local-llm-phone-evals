from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from typing import Any

from phone_eval_kit.redaction import redact_text


def adb_available() -> bool:
    return shutil.which("adb") is not None


def device_opted_in() -> bool:
    return os.environ.get("PHONE_EVALS_DEVICE") == "1"


def _run_adb(args: list[str], timeout: int = 15) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["adb", *args], text=True, capture_output=True, timeout=timeout, check=False)


def _authorized_devices() -> list[str]:
    if not adb_available():
        return []
    completed = _run_adb(["devices"])
    devices: list[str] = []
    for line in completed.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices


def _serial_hash(serial: str) -> str:
    return hashlib.sha256(serial.encode("utf-8")).hexdigest()[:16]


def _shell(serial: str, args: list[str], timeout: int = 15) -> str:
    completed = _run_adb(["-s", serial, "shell", *args], timeout=timeout)
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def _getprop(serial: str, name: str) -> str:
    return _shell(serial, ["getprop", name]).splitlines()[0:1][0] if _shell(serial, ["getprop", name]) else ""


def _parse_key_values(text: str, allowed_keys: set[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        normalized = key.strip().lower().replace(" ", "_")
        if normalized in allowed_keys:
            values[normalized] = value.strip()
    return values


def _meminfo_summary(text: str) -> dict[str, str]:
    allowed = {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}
    values: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key in allowed:
            values[key] = value.strip()
    return values


def _thermal_summary(text: str) -> list[str]:
    redacted_lines: list[str] = []
    for line in text.splitlines()[:20]:
        redacted, _ = redact_text(line.strip())
        if redacted:
            redacted_lines.append(redacted)
    return redacted_lines


def snapshot_device() -> dict[str, Any]:
    if not device_opted_in():
        return {"status": "skipped", "reason": "PHONE_EVALS_DEVICE is not set to 1"}
    if not adb_available():
        return {"status": "unavailable", "reason": "adb not found on PATH"}
    devices = _authorized_devices()
    if not devices:
        return {"status": "unavailable", "reason": "no authorized adb device"}
    serial = devices[0]
    battery = _shell(serial, ["dumpsys", "battery"])
    thermal = _shell(serial, ["dumpsys", "thermalservice"])
    meminfo = _shell(serial, ["cat", "/proc/meminfo"])
    return {
        "status": "collected",
        "serial_sha256_16": _serial_hash(serial),
        "manufacturer": _getprop(serial, "ro.product.manufacturer"),
        "model": _getprop(serial, "ro.product.model"),
        "device": _getprop(serial, "ro.product.device"),
        "android_release": _getprop(serial, "ro.build.version.release"),
        "android_sdk": _getprop(serial, "ro.build.version.sdk"),
        "battery": _parse_key_values(
            battery,
            {"level", "status", "health", "present", "temperature", "voltage", "powered"},
        ),
        "thermal_summary": _thermal_summary(thermal),
        "memory": _meminfo_summary(meminfo),
    }
