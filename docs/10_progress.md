# 進捗・次回の再開メモ

## 2026-10-01 — Discord → Terminal

**現在地：Phase 1の実装と、実際のDiscordからの直接メンション受信を確認済み。**
次は、通常投稿が表示されないことを実機で確認し、Phase 2のInbox保存へ進む。

### 今日できたこと

- Discordのテスト用ピアノ教室サーバー、カテゴリ、チャンネルを準備済み。
- Developer PortalでBotを登録し、テストサーバーへ追加済み。
- このexe.dev VMでPython Botを実行する構成を用意。`.venv`と依存関係は導入済み。
- 人がBotを直接メンションした投稿を受け取り、`source`・ユーザーID・チャンネルID・メッセージID・本文をターミナルへ表示。
- Botへのメンションを本文から除去。通常投稿、他Bot、Webhook、DMなどは対象外。
- 起動手順と設定例をREADMEに記載。

今回の処理は受信・表示まで。DB保存、LLM、返信、Calendar操作は未実装。
Discord固有の処理は受信モジュール内にあり、設計の責任分担は変更していない。

### 確認結果

- 自動テスト：**20件成功**。受信対象の判定、必須項目、表示整形、受信イベントから表示までを確認。
- トークン未設定時の起動エラー、依存関係の整合性、差分の空白チェックも確認済み。
- 実機：ユーザーがDiscordでBotをメンションし、VM側に次の結果が表示されたことを確認。実際のIDはメモへ転載しない。

```text
[RECEIVED]
source: discord
user_id: <取得できた>
channel_id: <取得できた>
message_id: <取得できた>
text: hello !
```

メンションなしの通常投稿を表示しないことは自動テストで確認済み。
**実機での通常投稿の確認結果は未記録**なので、次回の最初に確認する。

### 保存場所・Gitの状態

- 作業ディレクトリ：`/home/exedev/ss04_05_school-agent`
- 作業ブランチ：`feat/discord-receive`
- 実装コミット：`ac2c53e` — `feat: receive Discord secretary mentions`
- この日の作業ではローカルコミットまで実施。push・PR・mainへのマージは未実施。
- 受信コード：[discord_receiver.py](../src/school_agent/discord_receiver.py)
- テスト：[test_discord_receiver.py](../tests/test_discord_receiver.py)
- 依存関係：[pyproject.toml](../pyproject.toml)
- 起動手順：[README](../README.md)

VMの`.env`は実機確認に使用済み。既存の設定を使い、`.env.example`で上書きしない。
トークンと`.env`はGitの管理対象外とし、このメモにも記録しない。

### 次回の開始手順

1. このメモと[開発手順](08_development_workflow.md)を読み、現在のブランチと差分を確認する。

   ```bash
   cd /home/exedev/ss04_05_school-agent
   git status --short --branch
   git log -3 --oneline
   ```

2. Botを起動する。すでに起動中なら、そのターミナルを使う。

   ```bash
   .venv/bin/python -m school_agent.discord_receiver
   ```

3. `[READY]`の後、Discordで直接メンションした投稿が表示され、メンションなしの投稿は表示されないことを確認する。終了は`Ctrl+C`。
4. Phase 1の差分をレビューし、必要に応じてpush・PR・マージを行う。
5. 次のIssueの範囲を確認し、Inbox保存の実装へ進む。

### 次の最小Issue：受信メッセージをInboxへ保存

**目的：Discordで受信した直接メンションを、SQLiteの`agent_inbox`へ`pending`状態で保存する。**

- [データモデル](03_data_model.md)の`agent_inbox`を参照し、最小のSQLite保存処理を追加する。
- 保存対象は`source`、`external_user_id`、`channel_id`、`external_message_id`、`text`、`status`、`created_at`など。未処理時の`processed_at`・`error`はNULLを想定。
- 現在の`user_id`を`external_user_id`、`message_id`を`external_message_id`へ対応させる。
- Discord Adapterは受信・正規化を担当し、保存処理は別モジュールで担当する。
- 受入条件：1件の直接メンションで、正しいID・本文を持つ`pending`レコードが1件保存され、Botを終了してもDBに残る。
- 保存処理の自動テストと実機でのDB確認を行う。通常投稿は保存しない。
- 同一メッセージの重複受信、DB書き込み失敗の扱いは、実装開始時に小さく整理する。
- このIssueにもLLM・Agent Core・Outbox・自動返信・Calendar・Dotは含めない。

### 環境の申し送り

この日の作業中、VMの空き容量不足で仮想環境の準備が一度失敗した。
再取得可能な一時npmキャッシュを整理して作業を再開したが、最終確認時の空きは約184MB。
依存追加やDB作成に進む前に`df -h /home/exedev`で確認する。
