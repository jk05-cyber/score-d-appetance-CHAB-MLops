"""Convenience helpers for key paths."""
from pathlib import Path
from ..config import settings


def raw_file(name: str) -> Path:
    return settings.RAW_DIR / name


def processed_file(name: str) -> Path:
    return settings.PROCESSED_DIR / name


def scored_file(name: str) -> Path:
    return settings.SCORED_DIR / name
