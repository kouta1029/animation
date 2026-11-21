# 制作ルール v0.1

## 共同作業の原則
- 一次資料：`docs/decisions.md`、`docs/series_bible.md`、担当別仕様。
- Issueを起点に、作業ブランチ（例：`feat/art-character-rough`）→ PR → レビュー → mainへ反映。
- 重要設定は担当が独断で変更しない。総監督承認の変更は決定ログを更新する。
- 各チャットは自動同期されない。引継ぎにはIssue/PR番号、参照コミット、成果物パスを入れる。
- 権利不明のフォント、画像、BGM、音声、声クローンを採用しない。生成サービスの商用規約を記録。

## 制作ゲート
| ゲート | 主な担当 | 合格条件 |
|---|---|---|
| G0 企画 | 総監督 | オリジナル性・面白さ・尺・制作可能性 |
| G1 脚本 | 脚本監督→総監督 | 冒頭の魅力、人物の動機、オチ、設定矛盾なし |
| G2 絵コンテ・素材 | 演出監督＋作画監督→総監督 | ショット・表情・必要パーツ・構図が揃う |
| G3 音声 | 映像監督・総監督 | 話者・読み・感情・尺・権利条件が適正 |
| G4 試写 | 映像監督＋演出監督 | 口パク・身振り・字幕・カメラ・音声同期のQA |
| G5 公開承認 | 総監督 | 全編確認、権利、出力、YouTube掲載条件 |

## 引き継ぎ必須事項
```yaml
episode_id: EP001
role: art
source_commit: "<入力資料を読んだコミットSHA>"
source_docs: ["docs/series_bible.md"]
deliverables: ["assets/characters/..."]
status: draft
changes: "実施した作業"
unresolved: "未決定事項"
handoff_to: ["video", "direction"]
```

## 画音の品質
- Shorts：縦1080×1920、スマホUIに字幕が被らない、音声が聞き取れる。
- 長尺：横1920×1080、同構図が続きすぎない、冒頭と中盤に新しい展開。
- 24/30fpsを基準に同一作品内で統一。最終MP4はH.264/AACなど再生互換の高い形式で検証。
- 感情の変化に合わせ目・眉・口・腕・首・体、カメラを動かす。単純な微振動だけで済ませない。
- 実際に全編再生して表情・音割れ・途切れ・字幕欠け・画面端の欠けを確認する。

## 各話の基本成果物
`episodes/ep001/brief.md` → `script.md` → `shots.csv` → `audio_manifest.csv` → `asset_manifest.csv` → `qa.md` を基本とする。第1話の本制作はG0承認後。

## 技術（暫定）
Godotでカットアウト＋パーツ差し替え、必要ならBlender Grease Pencil。FFmpeg等で音声・字幕・書き出し。感情音声はElevenLabsを第一候補とし、VOICEVOX・AivisSpeechと日本語で比較。
