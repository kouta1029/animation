"""エージェント設定の静的検証テスト。実際のAI呼び出しはしない。"""
import tempfile
import unittest
from pathlib import Path

from tools.validate_codex_agents import ROOT, ROLES, validate


class CodexAgentTests(unittest.TestCase):
    def test_project_roles_and_docs(self):
        self.assertEqual(validate(ROOT), [])

    def test_exactly_four_custom_role_files(self):
        actual = {p.stem for p in (ROOT / ".codex" / "agents").glob("*.toml")}
        self.assertEqual(actual, set(ROLES))

    def test_missing_config_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate(Path(tmp))
            self.assertTrue(errors)
            self.assertIn("config.toml", errors[0])


if __name__ == "__main__":
    unittest.main()
