"""エージェント設定の静的検証テスト。実際のAI呼び出しはしない。"""
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.validate_codex_agents import ROOT, validate


class CodexAgentTests(unittest.TestCase):
    def test_project_roles_and_docs(self):
        self.assertEqual(validate(ROOT), [])

    def test_unexpected_role_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / ".codex", root / ".codex")
            shutil.copytree(ROOT / "docs", root / "docs")
            (root / ".codex" / "agents" / "extra.toml").touch()
            self.assertEqual(validate(root), ["未定義のロールファイル: extra.toml"])

    def test_art_quality_rules_reference_is_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / ".codex", root / ".codex")
            shutil.copytree(ROOT / "docs", root / "docs")
            path = root / ".codex" / "agents" / "art_director.toml"
            text = path.read_text(encoding="utf-8").replace("docs/roles/art/agent.md", "missing_art_rules.md")
            path.write_text(text, encoding="utf-8")
            errors = validate(root)
            self.assertTrue(any("作画品質ルールへの参照がありません: docs/roles/art/agent.md" in e for e in errors))

    def test_art_quality_checklist_must_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / ".codex", root / ".codex")
            shutil.copytree(ROOT / "docs", root / "docs")
            (root / "docs" / "roles" / "art" / "review_checklist.md").unlink()
            self.assertIn("必要な資料がありません: docs/roles/art/review_checklist.md", validate(root))

    def test_agents_must_be_a_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".codex").mkdir()
            (root / ".codex" / "config.toml").write_text("agents = true\n")
            self.assertEqual(validate(root), ["[agents] はTOMLテーブルにしてください"])

    def test_missing_config_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            errors = validate(Path(tmp))
            self.assertTrue(errors)
            self.assertIn("config.toml", errors[0])


if __name__ == "__main__":
    unittest.main()
