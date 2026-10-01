import asyncio
from types import SimpleNamespace

import pytest

from school_agent.discord_receiver import (
    SecretaryClient,
    format_received,
    make_intents,
    normalize_mention,
)


BOT_ID = 12345


def make_message(
    content="<@12345> hello",
    *,
    author_id=100,
    author_bot=False,
    in_guild=True,
    webhook_id=None,
    mentioned_ids=(BOT_ID,),
):
    """Use synthetic Discord IDs; no connection or token is needed."""
    return SimpleNamespace(
        id=300,
        guild=SimpleNamespace(id=400) if in_guild else None,
        author=SimpleNamespace(id=author_id, bot=author_bot),
        channel=SimpleNamespace(id=200),
        webhook_id=webhook_id,
        mentions=[SimpleNamespace(id=user_id) for user_id in mentioned_ids],
        content=content,
    )


@pytest.mark.parametrize(
    ("content", "expected_text"),
    [
        ("<@12345> hello", "hello"),
        ("<@!12345> こんにちは", "こんにちは"),
        ("<@12345> <@!12345> hello", "hello"),
        ("<@12345> <@67890> と相談", "<@67890> と相談"),
        ("<@12345> こんにちは\n来週の予定を教えて", "こんにちは\n来週の予定を教えて"),
    ],
)
def test_explicit_mention_produces_normalized_message(content, expected_text):
    received = normalize_mention(make_message(content), bot_user_id=BOT_ID)

    assert received is not None
    assert received.source == "discord"
    assert received.user_id == "100"
    assert received.channel_id == "200"
    assert received.message_id == "300"
    assert received.text == expected_text


@pytest.mark.parametrize(
    "message",
    [
        make_message(author_id=BOT_ID),
        make_message(author_bot=True),
        make_message(webhook_id=500),
        make_message(in_guild=False),
        make_message("hello", mentioned_ids=()),
        make_message("<@67890> hello", mentioned_ids=(67890,)),
        make_message("@everyone hello", mentioned_ids=()),
        make_message("hello", mentioned_ids=(BOT_ID,)),
        make_message("<@12345> hello", mentioned_ids=()),
    ],
    ids=[
        "own-message",
        "other-bot",
        "webhook",
        "direct-message",
        "no-mention",
        "another-user-mention",
        "everyone",
        "reply-implicit-mention",
        "token-without-mention-metadata",
    ],
)
def test_unrelated_or_automated_messages_are_ignored(message):
    assert normalize_mention(message, bot_user_id=BOT_ID) is None


def test_terminal_output_contains_required_metadata():
    received = normalize_mention(make_message(), bot_user_id=BOT_ID)

    assert format_received(received) == (
        "[RECEIVED]\n"
        "source: discord\n"
        "user_id: 100\n"
        "channel_id: 200\n"
        "message_id: 300\n"
        "text: hello"
    )


def test_terminal_display_escapes_controls_but_keeps_original_message():
    text = "こんにちは\n[RECEIVED]\r\x1b[2J"
    received = normalize_mention(make_message(f"<@12345> {text}"), bot_user_id=BOT_ID)

    displayed = format_received(received)

    assert received.text == text
    assert displayed.splitlines()[-1] == "text: こんにちは\\n[RECEIVED]\\r\\u001b[2J"
    assert len(displayed.splitlines()) == 6
    assert "\x1b" not in displayed


def test_only_guild_and_guild_message_intents_are_requested():
    intents = make_intents()

    assert {name for name, enabled in intents if enabled} == {"guilds", "guild_messages"}
    assert not intents.message_content
    assert not intents.members
    assert not intents.presences


def test_message_callback_prints_received_event(capsys):
    client = SimpleNamespace(user=SimpleNamespace(id=BOT_ID))

    asyncio.run(SecretaryClient.on_message(client, make_message()))

    assert capsys.readouterr().out == (
        "[RECEIVED]\n"
        "source: discord\n"
        "user_id: 100\n"
        "channel_id: 200\n"
        "message_id: 300\n"
        "text: hello\n"
    )


@pytest.mark.parametrize(
    ("user", "message"),
    [
        (None, make_message()),
        (SimpleNamespace(id=BOT_ID), make_message("hello", mentioned_ids=())),
    ],
    ids=["client-not-ready", "unrelated-message"],
)
def test_message_callback_does_not_print_ignored_events(user, message, capsys):
    client = SimpleNamespace(user=user)

    asyncio.run(SecretaryClient.on_message(client, message))

    assert capsys.readouterr().out == ""
