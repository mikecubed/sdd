"""Tests for sdd agent detection."""

from unittest.mock import patch

from sdd_cli.detect import detect_claude, detect_copilot


class TestDetectClaude:
    def test_returns_true_when_binary_found(self):
        with patch("shutil.which", return_value="/usr/local/bin/claude"):
            assert detect_claude() is True

    def test_returns_false_when_binary_not_found(self):
        with patch("shutil.which", return_value=None):
            assert detect_claude() is False


class TestDetectCopilot:
    def test_returns_true_when_binary_found(self):
        with patch("shutil.which", return_value="/usr/local/bin/copilot"):
            assert detect_copilot() is True

    def test_returns_false_when_binary_not_found(self):
        with patch("shutil.which", return_value=None):
            assert detect_copilot() is False
