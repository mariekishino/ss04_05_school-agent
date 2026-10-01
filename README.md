# School Agent

小規模ピアノ教室の事務を、Discord上の会話から扱うAI秘書のPoC。
最初のMVPはレッスン振替。設計は [Product Vision](docs/00_product_vision.md) と
[MVP Scope](docs/09_mvp_scope.md) を参照。

## 現在の実装: Phase 1 — Discord → Terminal

人がサーバー内でBotを直接メンションすると、IDと本文をターミナルに表示する。
DB保存、AIによる解釈、Discordへの返信、Calendar操作は後続のIssueで実装する。

## exe.dev VMでの準備

Python 3.10以上を使用する。プロジェクトのディレクトリで実行する。

```bash
cd /home/exedev/ss04_05_school-agent
python3 -m venv .venv
.venv/bin/python -m pip install --no-cache-dir -e '.[dev]'
```

`.env.example`を参考に、プロジェクト直下の`.env`をエディタで作成する。
`DISCORD_BOT_TOKEN=`の右側へDeveloper PortalのBotトークンを設定する。
トークンはチャットへ貼らず、Gitにコミットしない。`.env`はGitの追跡対象外。
環境変数にも同名の設定がある場合は環境変数が優先される。

```text
DISCORD_BOT_TOKEN=ここを実際のBotトークンに置き換える
```

Botが参加しているテスト用サーバーで、対象テキストチャンネルの
「チャンネルを見る / View Channel」権限をBotに与える。
非公開チャンネルではカテゴリ・チャンネル側の権限も確認する。
人側はそのチャンネルへメッセージを送信できる必要がある。

この実装ではGatewayの `guilds` と `guild_messages` だけを購読する。
Bot自身への直接メンションの本文は、Message Content Intentなしでも取得できるため、
今回の受信確認にPrivileged Gateway Intentsの有効化は不要。
これは[Discord公式のMessage Content例外](https://docs.discord.com/developers/events/gateway#message-content-intent)
を利用する。Botの送信権限・管理者権限も今回の処理には使わない。

## 起動と実機確認

```bash
.venv/bin/python -m school_agent.discord_receiver
```

`[READY] bot_user_id: ...`が表示されたら接続完了。
Discordで`@`を入力し、候補から**作成したBot自身**を選んで投稿する。
Botの名前がsecretary以外なら、その名前を選ぶ。

```text
@secretary hello
```

VMのターミナルに次のように表示される（IDは実際のDiscordの値）。

```text
[RECEIVED]
source: discord
user_id: 111111111111111111
channel_id: 222222222222222222
message_id: 333333333333333333
text: hello
```

- 自分のBotへのメンション部分を本文から取り除き、前後の空白を除去する。
- メンションなし、他のユーザー宛、ロール宛、`@everyone`、DM、BotやWebhookからの投稿は表示しない。
- 返信操作で自動付与されるメンションだけでは受け付けず、本文内の直接メンションを必要とする。
- 本文内の改行・制御文字は、表示時に `\n` や `\u001b` としてエスケープする。
- BotからDiscordへの返信は行わない。終了はVMのターミナルで`Ctrl+C`。

人が直接メンションした投稿で期待した5項目が表示され、通常の投稿では表示されないことを確認する。
本物の生徒データは使用せず、テスト用の内容を投稿する。

## 自動テスト

```bash
.venv/bin/python -m pytest -q
```

テストはDiscordへの接続・トークンを必要としない。
メンション判定、本文の整形、除外対象、受信イベントから表示までを確認する。

## 実装の責任範囲と制約

受信・Discord固有の判定・正規化は `src/school_agent/discord_receiver.py` に置く。
業務判断やAgent Coreはまだ実装していない。
今の段階ではメッセージを保存せず、重複排除・再処理・常駐起動も扱わない。
参加サーバー内でBotが閲覧できるチャンネルの直接メンションが対象。
Botのチャンネル権限でテスト対象を絞る。

実機でのDiscord受信は自動テストとは別に確認する。
