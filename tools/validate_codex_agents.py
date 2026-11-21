#!/usr/bin/env python3
"""Codex 4担当のプロジェクト設定を検査する（Python 3.11+）。

静的検査のみ。Codexの起動やクラウドサービスへの接続は行わない。
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = ("script_director", "art_director", "direction_director", "video_director")
REQUIRED_DOCS = (
    "docs/decisions.md",
    "docs/series_bible.md",
    "docs/production_rules.md",
    "docs/agent_orchestration.md",
    "docs/prompts/start_pilot.md",
    "docs/roles/director.md",
    "docs/roles/script.md",
    "docs/roles/art.md",
    "docs/roles/art/agent.md",
    "docs/roles/art/review_checklist.md",
    "docs/roles/art/director_review.md",
    "docs/roles/direction.md",
    "docs/roles/video.md",
)
FORBIDDEN_ROLE_OVERRIDES = {
    "approval_policy",
    "sandbox_mode",
    "model_provider",
    "mcp_servers",
}


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    config_path = root / ".codex" / "config.toml"
    try:
        with config_path.open("rb") as handle:
            config = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [f"{config_path}: {exc}"]

    settings = config.get("agents", {})
    if not isinstance(settings, dict):
        return ["[agents] はTOMLテーブルにしてください"]
    if settings.get("enabled") is not True:
        errors.append("[agents].enabled が true ではありません")
    threads = settings.get("max_concurrent_threads_per_session")
    if not isinstance(threads, int) or isinstance(threads, bool) or threads < 4:
        errors.append("[agents].max_concurrent_threads_per_session は整数4以上を指定してください")

    roles_dir = root / ".codex" / "agents"
    unexpected = sorted(path.name for path in roles_dir.glob("*.toml") if path.stem not in ROLES)
    if unexpected:
        errors.append(f"未定義のロールファイル: {', '.join(unexpected)}")

    for role in ROLES:
        path = roles_dir / f"{role}.toml"
        try:
            with path.open("rb") as handle:
                data = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"{path}: {exc}")
            continue

        if data.get("name") != role:
            errors.append(f"{path}: name は {role} を指定してください")
        for key in ("description", "developer_instructions"):
            if not isinstance(data.get(key), str) or len(data[key].strip()) < 30:
                errors.append(f"{path}: {key} が空または短すぎます")
        for key in FORBIDDEN_ROLE_OVERRIDES.intersection(data):
            errors.append(f"{path}: {key} はロールごとの設定で変更しないでください")
        text = str(data.get("developer_instructions", ""))
        if "docs/decisions.md" not in text:
            errors.append(f"{path}: 決定ログへの参照がありません")
        if role == "art_director":
            for required in ("docs/roles/art/agent.md", "docs/roles/art/review_checklist.md"):
                if required not in text:
                    errors.append(f"{path}: 作画品質ルールへの参照がありません: {required}")

    for rel in REQUIRED_DOCS:
        if not (root / rel).is_file():
            errors.append(f"必要な資料がありません: {rel}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"Codex設定チェック: FAIL ({len(errors)}件)")
        for item in errors:
            print(f"- {item}")
        return 1
    print(f"Codex設定チェック: PASS ({len(ROLES)}ロール, 必須資料 {len(REQUIRED_DOCS)}件)")
    print("※ 実際のサブエージェント起動・外部サービス接続は未検証です。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
