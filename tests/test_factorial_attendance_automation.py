"""Tests for factorial_attendance_automation following PEP8/pytest style."""

from pathlib import Path
import sys

import pytest
from selenium.common.exceptions import TimeoutException

sys.path.append(str(Path(__file__).resolve().parent.parent))
import factorial_attendance_automation as faa


def test_config_from_env_success(monkeypatch):
    """Load config successfully when all env vars are present."""
    monkeypatch.setenv("FACTORIAL_EMAIL", "user@example.com")
    monkeypatch.setenv("FACTORIAL_PASSWORD", "secret")
    monkeypatch.setenv("SHOW_BROWSER", "true")

    cfg = faa.Config.from_env()

    assert cfg.email == "user@example.com"
    assert cfg.password == "secret"
    assert cfg.show_browser is True


def test_config_from_env_missing(monkeypatch):
    """Raise ValueError when required env vars are missing."""
    monkeypatch.delenv("FACTORIAL_EMAIL", raising=False)
    monkeypatch.delenv("FACTORIAL_PASSWORD", raising=False)

    with pytest.raises(ValueError):
        faa.Config.from_env()


def test_retry_succeeds_after_failures(monkeypatch):
    """Retry decorator eventually succeeds after transient failures."""
    calls = []

    @faa.retry_on_failure(max_retries=3, backoff_factor=0.0)
    def flaky():
        calls.append("attempt")
        if len(calls) < 3:
            raise TimeoutException("temporary")
        return "ok"

    monkeypatch.setattr(
        "factorial_attendance_automation.time.sleep",
        lambda *_: None,
    )

    result = flaky()

    assert result == "ok"
    assert len(calls) == 3


def test_retry_raises_after_max_attempts(monkeypatch):
    """Retry decorator bubbles exception after max attempts."""
    @faa.retry_on_failure(max_retries=2, backoff_factor=0.0)
    def always_fail():
        raise TimeoutException("boom")

    monkeypatch.setattr(
        "factorial_attendance_automation.time.sleep",
        lambda *_: None,
    )

    with pytest.raises(TimeoutException):
        always_fail()


def test_bot_uses_default_selectors():
    """Bot initializes with default selectors when none provided."""
    cfg = faa.Config(email="u", password="p", show_browser=False)

    bot = faa.FactorialAutomationBot(cfg)

    assert isinstance(bot.selectors, faa.Selectors)


def test_cleanup_closes_driver():
    """Cleanup closes the webdriver when present."""
    cfg = faa.Config(email="u", password="p", show_browser=False)
    bot = faa.FactorialAutomationBot(cfg)

    class DummyDriver:
        """Minimal stub to verify quit is invoked."""

        def __init__(self):
            self.closed = False

        def quit(self):
            self.closed = True

    dummy = DummyDriver()
    bot.driver = dummy

    # Access internal cleanup to ensure driver shutdown in tests
    bot._cleanup()  # pylint: disable=protected-access

    assert dummy.closed is True
