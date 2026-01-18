"""
Tests for src.config
"""
import sys
from _pytest.monkeypatch import MonkeyPatch


def test_parallelism_default(monkeypatch: MonkeyPatch) -> None:
    from src.config import sites_path

    monkeypatch.setattr(sys, "argv", ["script.py"])
    assert sites_path.exists()
