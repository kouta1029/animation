# Codex マルチエージェント制作運用 v0.1

> これは**Codexセッション内での委譲を可能にする設定・運用手順**です。GitHub Issueを監視して自動的に起動する常駐サービスではありません。人間が最初に総監督Codexへ制作目標を渡すと、総監督が適切な担当をサブエージェントとして起用します。

## 起動する担当と設定

プロジェクトをCodexで開くと、`.codex/config.toml` と `.codex/agents/*.toml` のカスタムロールを参照できます。利用できる環境・バージョン・プロジェクトの信頼設定に依存します。

| ロール名 | ファイル | 役割・所有範囲 |
|---|---|---|
| 総監督（親セッション） | この文書、[総監督 agent.md](roles/director/agent.md) | 判断・委譲・調整・QA・承認待ち |
| `script_director` | `.codex/agents/script_director.toml` | 企画候補、脚本、セリフ演技 |
| `art_director` | `.codex/agents/art_director.toml` | 作画ラフ、パーツ、素材QA |
| `direction_director` | `.codex/agents/direction_director.toml` | 絵コンテ、カット、表情/カメラ |
| `video_director` | `.codex/agents/video_director.toml` | 映像実装、音声同期、書き出し |

モデル名は指定しない。Codex側で利用可能なモデルを引き継ぐ。4担当同時起用の上限は`max_concurrent_threads_per_session = 4`であり、**必ず4人同時に起動する意味ではない**。細かい作業は親が自分で行い、分離できる作業にのみ委譲する。

## 親（総監督）が毎回行うこと

1. `docs/decisions.md`→`docs/series_bible.md`→`docs/production_rules.md`→`docs/roles/director.md`を読む。[制作フロー設計書](production_workflow.md)、AGENTS.md、担当の agent.md と品質チェックリストを追加で確認する。
2. 最新`main`、Issue、オープンPR、各担当の作業範囲を確認。参照コミットを記録する。PR #8（作画）等の未マージ成果物を勝手に承認・置換しない。
3. 依頼を話数・尺・候補・承認段階に分解し、各担当の**明確な入力と出力**を決める。対象ファイルの所有者を割り当てる。
4. 独立した調査・ラフ・技術検証は並行で委譲可能。依存する制作（脚本→絵コンテ→映像）は承認ゲートを通して順番に進める。
5. サブエージェントの成果物を回収し、設定の矛盾、同じファイルへの競合、権利・テスト結果を評価する。
6. 次担当へ受渡しする際、Issue/PRまたは成果物のパス、参照コミットSHA、受入条件、未決事項を添える。
7. G0～G5の承認が必要な事項は人間の決定を求める。契約、権利不明素材、YouTube公開、mainへの未承認マージは行わない。
8. 最後にステータスを「提案中 / 試作中 / PR作成 / レビュー待ち / 承認済み / ブロック中」で正確に報告する。

## 標準フロー

```text
人間：企画の方向性・投稿形式・制約・承認
          |
  総監督Codex（親セッション）
          |
          +-- 並行可能な事前調査・案出し ----------------+
          |   script_director: プロット候補             |
          |   art_director: キャララフ・差分試作         |
          |   video_director: 技術・音声・出力の検証      |
          |   direction_director: 絵コンテ雛形/演出案    |
          +---------------------------------------------+
          |
       G0：企画承認
          |
       script_director: 本脚本 → G1
          |
       direction_director: 絵コンテ   art_director: 必要素材
       video_director: 候補音声と実測尺を共有
                    \              /
                       G2a・G2bの確認 → G2最終承認
                          |
       G3：採用音声の承認
       video_director: 本制作 → G4
                          |
       総監督：G5公開前の最終レビュー（人間承認）
```

**並行化の例外**：設定の仮案を複数担当が編集しても合意済みにはしない。音声・映像で確定脚本やパーツの欠陥が分かったら、元担当へ修正要求を戻す。

## 出力所有権と競合防止

| ファイル | 主に書き換える担当 |
|---|---|
| `docs/decisions.md`, `docs/series_bible.md` | 総監督（承認済み変更のみ） |
| `episodes/ep###/brief.md`, `script.md` | 脚本監督（企画ブリーフ確定は総監督） |
| `assets/**` | 作画監督 |
| `episodes/ep###/shots.csv`, `storyboards/**` | 演出監督 |
| `animation/**`, `audio/**`, `renders/**` | 映像監督 |

複数エージェントはワークスペースを共有することがあるため、**同一ファイルを複数担当に同時編集させない**。競合する場合は順番に委譲するか、別worktree・ブランチを利用する。

## 指示の書式（親から子）

役割名、目的、入力のパスと版、出力パス、対象外のファイル、受入条件、報告形式を明記する。

```yaml
role: script_director
episode_id: EP001
goal: "50秒Shortsの脚本ラフを2案作る"
inputs:
  - "docs/decisions.md"
  - "docs/series_bible.md"
outputs:
  - "episodes/ep001/script_proposals.md"
read_only_paths:
  - "docs/decisions.md"
  - "docs/series_bible.md"
acceptance:
  - "各案が単独で面白く、フック・展開・オチがある"
  - "未承認の設定を確定しない"
report:
  - "参照コミット"
  - "成果物パスと検証内容"
  - "未解決点と次担当"
```

## 最初の1本の着手方法

1. Issue #10 とPR #9の状態を確認する。PR #9が未マージの場合は、その内容を参照して、導入後にルールを統合する。
2. `python tools/validate_codex_agents.py`を実行し、設定の静的検査をする。
3. Codexでリポジトリを開き、[総監督起動プロンプト](prompts/start_pilot.md)を入力する。
4. 親エージェントがG0準備のための独立タスクを委譲し、担当者の成果と未決事項を統合する。
5. G0を人間が承認したら、脚本→絵コンテ／素材→映像の順に進める。

## 検証範囲と限界

- **検証できること**：TOMLの構文、カスタムロール名、必要文書の存在、CIでの設定整合性。
- **実際のCodexでのみ確認できること**：子エージェントの起動、ツール権限、モデルの利用可否、並列実行、GitHub認証、画像生成、ElevenLabs等の外部サービス利用。
- **このPRだけでは行わないこと**：GitHub ActionsからのCodex自動起動、課金・APIキー登録、全自動YouTube投稿、PR自動マージ。
- **GitHub上のIssue作成がサブエージェント起動を保証するわけではない**。常駐・イベント駆動自動化は別の実装が必要。

## 参照（公式）

- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/config-file/config-reference
- https://developers.openai.com/api/docs/guides/agents-api/multi-agent
