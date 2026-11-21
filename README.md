# animation｜『もしも区の日常』（仮）

日本語YouTubeのオリジナル2Dアニメ（Shorts＋長尺）を、**総監督・脚本監督・作画監督・演出監督・映像監督**の5部門で制作する共通リポジトリ。

**方向性**：普通の住民が主人公の**日常×SFコメディ**。奇妙な世界のルールに振り回されながら日常を続ける姿を描き、Shortsで新規視聴者を、長尺で作品のファンを増やす。

## 必読

1. [決定事項・未決定事項](docs/decisions.md) — **判断の正本**
2. [シリーズバイブル](docs/series_bible.md) — 世界観と作品コンセプト
3. [制作ルール](docs/production_rules.md) — 役割分担と承認ゲート
4. [チャンネル総合設計書v1.0（原本DOCXからの抽出）](docs/source/channel_design_v1.0_extracted.txt) — 初期案。後の決定より優先しない
5. [作画監督向けキャラクターデザイン・パーツ仕様v0.1](docs/character_design_parts_v0.1.md) — デザイン詳細は未承認

## 共有リンク

- [Google 共有リンク](https://share.google/DeXexu7AHVPerTWCC)

## 5部門

| 部門 | 作業ガイド | 成果物 |
|---|---|---|
| 総監督 | [director](docs/roles/director.md) | 企画・品質・進行の承認 |
| 脚本監督 | [script](docs/roles/script.md) | あらすじ・脚本・セリフID |
| 作画監督 | [art](docs/roles/art.md) | 設定画・表情・分割パーツ |
| 演出監督 | [direction](docs/roles/direction.md) | 絵コンテ・動作・カメラ |
| 映像監督 | [video](docs/roles/video.md) | 2D実装・音声同期・MP4 |

## フォルダ

`docs/` 共有資料と役割ガイド  
`episodes/` 話数別脚本とショット台帳  
`assets/` キャラクター・背景・小物  
`audio/` 音声・BGM・SE・利用規約  
`animation/` アニメ制作プロジェクト  
`renders/` 映像の納品・QA

## 運用

- チャット間は自動同期されない。**GitHubの承認済み文書を正本**とする。
- 変更はIssue → ブランチ → PR → レビューを基本とする。
- 設定・名前・姿などの**仮案を確定扱いしない**。
- 企画・演技・独自性の品質を、投稿本数より優先する。
- カバとフラミンゴは過去の制作試作であり、新シリーズの固定キャラクターではない。

初期セットアップ：2026-11-21
