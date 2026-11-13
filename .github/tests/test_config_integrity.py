"""Check configuration bytes without importing or executing JavaScript."""
from pathlib import Path
from hashlib import sha256
import unittest

CONFIG = 'explorer/eslint.config.js'
EXPECTED_SHA256 = '4efe97b16d1200fac0eaf07aa00930a8668b1f96a0be1891ace8c1e712ff0ccb'
# Reviewed predecessor blob: 5e6b472f583e34a1cca751440d4f241495475723


def check_config_bytes(raw):
    if sha256(raw.replace(b"\r\n", b"\n")).hexdigest() != EXPECTED_SHA256:
        raise ValueError("Configuration differs from its reviewed pre-tail declarations")


class ConfigIntegrity(unittest.TestCase):
    def test_actual_config_has_only_reviewed_declarations(self):
        root = Path(__file__).resolve().parents[2]
        check_config_bytes((root / CONFIG).read_bytes())

    def test_executable_tail_is_rejected_without_execution(self):
        root = Path(__file__).resolve().parents[2]
        raw = (root / CONFIG).read_bytes()
        with self.assertRaises(ValueError):
            check_config_bytes(raw + b"\n(() => { throw new Error('untrusted tail'); })();\n")

    def test_create_require_injection_is_rejected_without_execution(self):
        root = Path(__file__).resolve().parents[2]
        raw = (root / CONFIG).read_bytes()
        with self.assertRaises(ValueError):
            check_config_bytes(b"import { createRequire } from 'module';\n" + raw)


if __name__ == "__main__":
    unittest.main()
