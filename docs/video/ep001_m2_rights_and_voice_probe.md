# EP001 M2の権利調査とAivisSpeechローカル音声実測

**映像監督 / 2026-11-22 / Issue #5 / 総監督指示**  
https://github.com/kouta1029/animation/pull/30#issuecomment-7078927682

## 制作上の正本と安全状態

- **G1承認対象**: PR #29 commit 7a349c981767f609124884f0ebe063899412d428 / episodes/ep001/rewrite_v1.3/A_rebound.md。総監督のG1コメント: https://github.com/kouta1029/animation/pull/29#issuecomment-7078754226
- **配役の仮指定**: PR #30 HEAD 09971f44dc8d2029f4103bfba96cedfcee2724b8 の voice_cast.md (主人公=にせ/ノーマル、友人=M2/ノーマルを候補)。
- **未承認**: M2のG3本採用、合成音声の収益化公開、正式な絵コンテ・作画・動画公開、mainマージ。
- **実機未実施**: ユーザーのWindowsで起動したAivisSpeech Engineにはこの作業環境から接続できないため、数値ID、実WAV生成、自然な発話長、視聴・聴取はすべてNOT_RUN。

## 一次規約の証跡とM2収益化判断

| 証拠 | 根拠・URL | 判断 |
| --- | --- | --- |
| AivisHub M2 | https://hub.aivis-project.com/aivm-models/d1a7446f-230d-4077-afdf-923eddabe53c | 「Style-Bert-VITS2に付属のデフォルト男性２モデル」「CC BY-SA 4.0のため再配布」、モデル制作者litagin。ただし表示ライセンス分類は「カスタムライセンス」。モデルUUID d1a7446f-230d-4077-afdf-923eddabe53c、話者UUID 6c831a4b-a90c-4a88-9083-b473c25f69ec。 |
| 原作者のモデル規約 | https://github.com/litagin02/Style-Bert-VITS2/blob/master/docs/TERMS_OF_USE.md | デフォルトJVNVモデル(jvnv-M2-jp含む)は、JVNVコーパス由来のCC BY-SA 4.0を継承すると明示。 |
| 原作者配布 | https://huggingface.co/litagin/style_bert_vits2_jvnv | license: cc-by-sa-4.0、およびJVNVコーパスのライセンス継承を表示。 |
| CC公式本文 | https://creativecommons.org/licenses/by-sa/4.0/deed.ja と https://creativecommons.org/licenses/by-sa/4.0/legalcode.ja | 商用利用を含む共有・翻案を許諾。表示・リンク・改変表示・対象の翻案物の同条件継承等が条件。その他の権利は別途検討。 |
| Hubの利用規約 | https://hub.aivis-project.com/terms-of-service/ 第10条 | ダウンロードモデルには当該モデルに付与されたライセンス条件が適用される。Engineの商用利用可否とは分離。 |

**評価**: M2の開発元がCC BY-SA 4.0を付与したことを一次資料で確認でき、当該ライセンスには非営利限定はないため、モデルの営利利用自体は条件付きで認められると考えられる。**ただし** AivisHubの「カスタムライセンス」欄がどの規約本文を意味するか、当該合成音声自体が翻案物になるか、YouTube映像と同期させた場合の継承範囲、帰属表示の具体的な対象および原音声の他の権利が未確認。「どんな収益化動画にも無条件で使用可」とは判定しない。

**対応**: G3本採用と収益化公開を保留し、配布者・原権利者に、合成音声の収益化利用、必要なクレジット、編集・音声再配布、CC BY-SAの継承範囲（音声のみか動画全体か）、権利者の範囲を確認。正式クレジットと利用条件を記録して総監督G3判定を受ける。仮の説明欄案（未承認）: 音声モデル M2 / Style-Bert-VITS2 JVNV model (litagin), CC BY-SA 4.0 / model URL 上記 / license https://creativecommons.org/licenses/by-sa/4.0/ / AI合成・編集有。

## G1承認済みPR #29 A稿の5発話（PR #30とは混ぜない）

| line_id | 話者 | モデル / 話者UUID | 台詞 | 仮枠 |
| --- | --- | --- | --- | --- |
| L01 | protagonist | にせ / bf56410a-d8e6-430d-a477-f789e16206d3 | 近っ | 07.10–07.90 = 0.80秒 |
| L02 | protagonist | にせ / 同上 | ちゃんと断ろ | 17.80–19.10 = 1.30秒 |
| L03 | organizer | M2 / 6c831a4b-a90c-4a88-9083-b473c25f69ec | お、来た | 37.40–38.60 = 1.20秒 |
| L04 | organizer | M2 / 同上 | 飲み物取って | 39.10–40.80 = 1.70秒 |
| L05 | protagonist | にせ / 同上 | 布団から誘うな！！ | 41.40–43.50 = 2.10秒 |

**重大なID衝突**: PR #30候補稿のL02/L03は友人、L04は主人公だが、G1承認PR #29ではL01/L02/L05=主人公、L03/L04=友人。PR #30の39.00–39.55秒「お、来た」の**0.55秒**は未承認稿の仮枠。PR #29の承認稿は37.40–38.60秒の**1.20秒**。0.55秒に無理に圧縮しない。実発話が1.20秒にも収まらない場合、演出監督へR13-07〜09のカット尺見直しを依頼。

モデルUUIDおよびAivisHubのモデル内Style ID 0をEngineのAPI数値IDとして使わない。GET /speakers の話者名とspeaker_uuidを完全照合してstyles[].idを取得する。にせHubの話者UUID参照: https://hub.aivis-project.com/aivm-models/6d11c6c2-f4a4-4435-887e-23dd60f8b8dd

## Windows 11ローカル実行手順

AivisSpeech Engineを起動し、にせ・M2をモデルとして導入したうえで、ブラウザで http://127.0.0.1:10101/speakers を開く（ローカルの実ポートが異なる場合はスクリプトの--urlで変更）。

リポジトリルートのPowerShellから次を実行（Python標準ライブラリのみ、追加pip不要）。

    python tools/video/ep001_aivis_local_probe.py --out "$env:USERPROFILE\Documents\ep001_voice_probe"

まず実際のspeaker/style数値IDだけを読み取る。必要なspeaker_uuidや「ノーマル」が見つからなければ明示的に停止し、無言の代替はしない。成功するとspeakers_resolved.jsonを出力。

仮の非公開音声5本を生成・実測するときだけ、次を実行。

    python tools/video/ep001_aivis_local_probe.py --out "$env:USERPROFILE\Documents\ep001_voice_probe" --render

生成されるもの: PR29_A_Lxx_話者.wav 5本、provisional_audio_manifest.csv、measurement.json。話速は変更せず、出力WAVをそのまま保存。10ms窓・-40dBFS閾値による有声部の近似長と先頭/末尾無音を計測。超尺なら RETIME_REQUIRED を記録し、早口や有声部分の音声切断は禁止。計測結果だけで自然な発音とは言えないため、人間の試聴（促音、読み、声の温度差、語尾、クリッピング）が必要。

**音声ファイルと原モデルは公開リポジトリにコミットしない。** 作業成果はQC数値・権利情報・必要なカット尺調整依頼として連携する。

## QA・引き継ぎ

- Pythonコードの構文検査・単体テスト3件（誤UUIDの拒否、実数値style IDの選択、PCM WAV長と前後無音の測定）: **PASS（ローカルのモック／テスト波形のみ）**。
- AivisSpeech実機 /speakers, にせ・M2の本当の数値ID、WAV5本の生成・実尺・耳による聴取: **NOT_RUN**。
- 演出監督: L03とL04とL05の自然な発話の開始/終端、0.4秒以上の表情余韻を受けてR13-07〜09を再配分。言葉を削る必要があるなら脚本のG1差分再審査へ。
- 総監督: M2の合成音声収益化利用・表示義務と継承範囲が確定し、聴取・実尺QCを確認してからG3採否を判定。本報告はマージ・正式音声・公開を承認しない。
