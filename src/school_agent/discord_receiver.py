"""Phase 1: receive explicit Discord mentions and print normalized metadata."""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import discord
from dotenv import load_dotenv


@dataclass(frozen=True)
class ReceivedMessage:
    source: str
    user_id: str
    channel_id: str
    message_id: str
    text: str


def normalize_mention(
    message: discord.Message, *, bot_user_id: int,
) -> ReceivedMessage | None:
    """Accept human server messages with an explicit mention of this bot."""
    if (
        message.guild is None
        or message.author.bot
        or message.author.id == bot_user_id
        or message.webhook_id is not None
    ):
        return None
    if not any(user.id == bot_user_id for user in message.mentions):
        return None

    mention = re.compile(rf"<@!?{bot_user_id}>")
    if not mention.search(message.content):
        # A reply can mention its author in metadata without an explicit body mention.
        return None

    return ReceivedMessage(
        source="discord",
        user_id=str(message.author.id),
        channel_id=str(message.channel.id),
        message_id=str(message.id),
        text=mention.sub("", message.content).strip(),
    )


def format_received(event: ReceivedMessage) -> str:
    # Keep Japanese readable while escaping newlines and terminal escape characters.
    display_text = json.dumps(event.text, ensure_ascii=False)[1:-1]
    return (
        "[RECEIVED]\n"
        f"source: {event.source}\n"
        f"user_id: {event.user_id}\n"
        f"channel_id: {event.channel_id}\n"
        f"message_id: {event.message_id}\n"
        f"text: {display_text}"
    )


def make_intents() -> discord.Intents:
    intents = discord.Intents.none()
    intents.guilds = True
    intents.guild_messages = True
    return intents


class SecretaryClient(discord.Client):
    async def on_ready(self) -> None:
        if self.user is not None:
            print(f"[READY] bot_user_id: {self.user.id}", flush=True)

    async def on_message(self, message: discord.Message) -> None:
        if self.user is None:
            return
        event = normalize_mention(message, bot_user_id=self.user.id)
        if event is not None:
            print(format_received(event), flush=True)


def main() -> int:
    # Read only this working directory's .env; explicitly exported variables win.
    load_dotenv(dotenv_path=Path.cwd() / ".env")
    token = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    if not token:
        print("DISCORD_BOT_TOKEN を .env または環境変数に設定してください。", file=sys.stderr)
        return 1

    client = SecretaryClient(intents=make_intents())
    try:
        client.run(token)
    except discord.LoginFailure:
        print("Botにログインできませんでした。DISCORD_BOT_TOKEN を確認してください。", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
