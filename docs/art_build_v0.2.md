# 作画部門：正面カットアウト素材試作 v0.2

**状態：G2_PENDING** — キャラデザインは総監督・演出監督が未承認です。正式設定には使用しません。

## 手元で生成
Python 3.10+：
- `python -m pip install -r requirements-art.txt`
- `python tools/art/build_assets.py --output build/art_v0.2`
- `python tools/art/qa_assets.py build/art_v0.2`

**生成数：** 3人×64 SVG、同数の透過PNG。基本レイヤー13、目8種、眉7種、口10種、完成形表情10種、マスターSVG1/人。全PNGは共通位置合わせのため750×2000（SVG基準600×1600）。`asset_manifest.json`に色・位置・暫定ピボットを記録。

## 関係資料
- `docs/decisions.md`：承認済みの決定事項（本PRは変更しません）
- `docs/character_design_parts_v0.1.md`：原案
- `docs/art_direction_v0.2.md`：作画方針と承認項目
- `docs/handoff_v0.2.md`：他部門への引き継ぎ
- `tools/art/build_assets.py`：再現可能なベクター/透過PNG生成コード
- `tools/art/qa_assets.py`：自動検査

## 未制作/未検証
正面のみの概念リグです。左右3/4、腕6ポーズ、左右手5種、上腕/前腕/手の関節分離、走行/歩行、背景、レイヤー付きPSD、本番動画のGodot実機検証は含みません。生成AIのコンセプト画像とSVG試作は同一デザインではなく、別途アートディレクションが必要です。

生成物はGitHub Actionsのartifactsからも取得できます（CIが通過した場合）。
