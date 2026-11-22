# EP001 G1前・映像技術試作の検証記録

担当: 映像監督 / Issue #5 / 連携 PR #18  
入力: d6d263ec7850d9f1b88d3bbf03a83d695684fa2a（script.md、ikitara_previs_plan.md、technical_plan.md、art_requirements.md）。G0承認、G1審査中。  
区分: **技術試作のみ。正式コンテ・作画・G3音声・公開候補ではない。**

## 再現手順
Python 3、Pillow、FFmpeg・ffprobe（PATH）、Noto Sans CJK JP Regular のフォントファイルを準備。フォントは同梱しない。Linux実測は Pillow 12.3.0、FFmpeg 7.1.5。Noto Sans CJK は SIL OFL 1.1（https://github.com/notofonts/noto-cjk/blob/main/LICENSE）、正式作品での採用判断は別途行う。
    
Linux: リポジトリルートから実行:
    
    python -m pip install Pillow==12.3.0
    python animation/pilot/ikitara/probe/render_probe.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc --out /tmp/ikitara-probe

Windows PowerShell: Python、FFmpeg/ffprobe、上記の日本語フォントを用意し、実在するパスを指定:
    
    python -m pip install Pillow==12.3.0
    python animation/pilot/ikitara/probe/render_probe.py --font "C:\path\to\NotoSansCJK-Regular.ttc" --out "$env:TEMP\ikitara-probe"

Windowsは手順のみ、本環境で未実行。生成物は probe.mp4、360x640の8枚のPNG、qa.json。出力先はリポジトリ外とし、MP4やフォントはコミットしない。

## 実測結果 (2026-11-22)
Linux上で実行。1080x1920 / 24fps / 840 frames / 35.000000s / H.264 yuv420p / 音声なし（意図的）。ffmpeg -v error -xerror による全編デコードとffprobeによるフレーム数照合 PASS。

| 検証 | 結果と範囲 |
|---|---|
| 戸枠マスク | PASS: CPU Pillow矩形クリップ。8時点で外壁・枠・前景代理図形の検査座標を照合。接近停止時に店が開口幅を超えても外壁を保持。Godotの描画ではない。 |
| 遠方・接近・停止・消失 | PASS: 代表座標と360px幅の代表6フレームを目視。2.2 / 6.2 / 8.5 / 18 / 25 / 30秒。消失前24.5と後25秒で前景・戸の検査座標不変。 |
| メッセージ・貼り紙 | PASS: 48pxフォント、字送り幅 M01=384 M02=288 M03=336 M04=240 M05=528 M06=480 S01=240 px、660px以下。6メッセージの表示位置をコードで検査。代表画像では貼り紙が戸と重ならない。 |
| 実端末UI、初見者の無音理解、全編の人間による実再生 | NOT_RUN: 代表画像目視とデコードのみ。UIガイドは仮の位置。 |
| Godot CanvasItem/Control実描画、Windows、斜めマスク、正式素材の関節 | NOT_RUN: Godot未設置・素材未承認。 |
| 発話L01/L02、候補音声の生成・利用条件・字幕同期 | NOT_RUN: G1承認待ち。発話字幕も今回は表示しない。 |
| 作画QC・G4/G5 | N/A: 代理図形による技術試作。作画監督のデザインを置換しない。 |

## 仮イベント時刻
M02 .90秒表示、戸開き1.15〜2.05、M03表示4.5・接近5.0〜7.4、M04表示14・戸閉めかけ16.2〜17、S01表示17〜24.65（脚本の22秒以降は消失確認のため延長した技術試作。正式タイムラインには反映しない）、M05表示24・消失24.65、M06表示29〜32.1。カメラ固定。のれんの揺れ、廊下の実際の縮み、キャラの芝居は未実装。手は青色の矩形で遮蔽順確認のみ。正式な演出・形状・配色を提案しない。

## 次の担当・ブロッカー
演出: 無音初見・実端末で文字の滞留と因果を確認。S01の表示終了は脚本と正式コンテに合わせる。
作画: 戸枠、扉、廊下の遠近、店、のれん、貼り紙の分離素材と手のピボットを承認後に提供。
映像: G1後にL01/L02の候補比較・権利記録。Godot実描画と正式素材の遮蔽を確認し、G2/G3後に本制作。
総監督: 本PRは技術試作の審査のみ。ゲート承認・mainマージ・公開しない。

成果物のMP4と比較画像はチャットで共有。GitHubには再現コードと実測記録を提出。
