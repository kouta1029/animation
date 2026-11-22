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

## G2審査用の設定画リンクと素材対応

| 役割／画角 | 審査用の画像 | 現状の生成リグ対応 |
| --- | --- | --- |
| ナオ：正面・左右3/4 | [nao_turnaround.svg](../assets/concepts/v0.3/nao_turnaround.svg) | 正面のみ v0.3 リグ対応。3/4は静止ラフ |
| ヒビキ：正面・左右3/4 | [hibiki_turnaround.svg](../assets/concepts/v0.3/hibiki_turnaround.svg) | 正面のみ v0.3 リグ対応。3/4は静止ラフ |
| スズ：正面・左右3/4 | [suzu_turnaround.svg](../assets/concepts/v0.3/suzu_turnaround.svg) | 正面のみ v0.3 リグ対応。3/4は静止ラフ |
| 3人の128px比較 | [compare_128px.svg](../assets/concepts/v0.3/compare_128px.svg) | 同じ縮尺（360×600座標系を128px高に縮小）で9体を比較 |

### 画像の生成・検査
```bash
python tools/art/qa_concept_views.py --render build/art_v0.3/concepts
```

- 静止設定画は`assets/concepts/v0.3/*.svg`に格納済み。GitHub上のリンクから直接閲覧できる。
- 描画確認用PNGはGitHub Actionsの`art-v0.3-redesign-unapproved-svg-png`から取得可能（Artifact保持期間は7日）。
- 128px比較は各キャラクター・各向きに**同一の縮小比 128/600**を適用。自動QAはファイル構造・縮尺・レンダリングのみ確認する。
- 3/4右は左3/4の鏡像ラフ。衣装小物の配置、可動リグの奥行、遮蔽、向きによる前後関係は未検証。
- 新しい3方向のラフを`tools/art/build_assets.py`が生成する正面カットアウト実装へ統合する工程は**別途必要**。

## 未実装
3/4向き・手の独立パーツ・歩行/走行・PSD・Godot実機確認。生成したデザイン試作とChatGPT内のコンセプト画像は別素材であり一致を保証しません。総監督G2承認までマージせず、正式素材扱いもしません。
