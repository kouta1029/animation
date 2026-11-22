# v0.5 画像原本の移管状況

**BLOCKED_ASSET_UPLOAD / 未承認（2026-11-22）**

作画監督のチャット環境で以下の実ファイルを作成・目視し、ZIPを作成済み。GitHub接続の文章用APIで画像バイナリ転送を完了できないため、本PRには画像自体を含めない。画像がGitHubに存在すると誤認させないこと。

## ローカルパックの内容（ファイルは別途共有）

| 内容 | 格納先（ZIP内） | SHA-256 |
|---|---|---|
| オーナー基準画像 | `assets/reference_owner.png` | `2a7b9d999b09565fa5100bfeca15d752bc6bd1c9e19ad90ea42c9bd31388b359` |
| v0.5独自絵柄キービジュアル原画 | `assets/v05_signature_keyvisual.png` | `fce27a01eef32905d0ad51edb361a4133391af736c6f9149052b2ec7874cc686` |
| 原寸画像の配置比較 | `qa/full_reference_vs_v05.jpg` | `0d28883c7fcff731ddddde292775e5898528476fbd6b7c5df6f9db3beeab5d8c` |
| 顔のクロップを128px高にした比較 | `qa/face_compare_128px.png` | `039e2af075494325812cdb171a21f2f830dfcfaed5a4e672ac4abc4cef0ebd93` |
| 判定・検査記録 | `docs/README.md`, `docs/manifest.json` | ZIP内 |

パック名：`art_identity_v05_preapproval.zip`（本チャットの成果物）。ZIP内全ファイルのCRC検証と元PNG2枚・比較PNG/JPEGの画像読み込み検査はPASS。今回の試験は顔クロップを128px高にしたもので、全身128px高の審査資料は**未制作**。

## 登録・レビューの再開条件
1. GitHubリポジトリにPNG/JPEGを実アップロードし、上記SHA-256を照合。ファイルURLが開けることを確認。
2. `docs/art/visual_identity_v0.5.md` の比較・修正要件と画像の版を対応づける。
3. 正面・左右3/4の「設定画」と、背景込みのマーケティング用キーアートを区別する。
4. 作画QCに不合格項目が残るため**総監督デザイン一次承認をまだ求めない**。正式配役の仮指示は画像の採用承認とは異なる。

この文書をPRの納品証明やバイナリ登録の完了証明として扱わない。
