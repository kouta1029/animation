# 作画v0.3：独自性強化ラフの生成・検証

このブランチはPR #6（v0.2）を置き換える **G2_PENDING** の作画試作です。未承認キャラデザインであり、正式公開用素材ではありません。

## 再生成
```bash
python -m pip install -r requirements-art.txt
python tools/art/build_assets.py --output build/art_v0.3
python tools/art/qa_assets.py build/art_v0.3
```

## 出力
- 3人（nao / hibiki / suzu）
- 各キャラ66 SVG + 66 RGBA PNG、合計198 + 198。
- ベース15レイヤー（新規：`signature_hair`、`signature_costume`）、目8、眉7、口10、表情10。
- SVGは600×1600、PNGは750×2000。差し替えレイヤーも共通座標で出力。
- `asset_manifest.json` に配色・G2ステータス・構造・暫定ピボットを記録。

## 参照
- `docs/art_direction_v0.3.md`：新デザインの狙い、3人の固有形状、未承認事項。
- `docs/character_design_parts_v0.1.md`：元のパーツ要求。
- `docs/decisions.md`：承認済み決定事項（このブランチでは変更しない）。
- `docs/art_build_v0.2.md`：履歴参照用旧稿。現行のビルド指示はこの文書を優先する。

## 未実装
3/4向き・手の独立パーツ・歩行/走行・PSD・Godot実機確認。生成したデザイン試作とChatGPT内のコンセプト画像は別素材であり一致を保証しません。総監督G2承認までマージせず、正式素材扱いもしません。
