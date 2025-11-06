"""Console helper to log into Telegram via Telethon and list available chats.

The script loads API credentials from a local `.env` file that contains
`TELEGRAM_API_ID` and `TELEGRAM_API_HASH`. The Telethon session is stored in
`telegram.session` (or whatever name you pick below) so that subsequent runs
reuse the saved login when possible.
"""

from __future__ import annotations

import asyncio
from datetime import timezone
from pathlib import Path
from typing import Dict, Iterable, Sequence

from telethon import TelegramClient


ENV_FILE = Path(".env")
SESSION_NAME = "telegram"  # Stored as `telegram.session` in the working dir.


def load_env(file_path: Path) -> Dict[str, str]:
    """Tiny .env parser so we do not depend on `python-dotenv`.

    Only supports simple KEY=VALUE pairs; lines starting with `#` are ignored.
    Surrounding quotes are stripped and whitespace is trimmed.
    """

    data: Dict[str, str] = {}

    if not file_path.exists():
        raise FileNotFoundError(
            f"Could not find {file_path!s}. Create it with TELEGRAM_API_ID and TELEGRAM_API_HASH."
        )

    for raw_line in file_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"\'')
        if key:
            data[key] = value

    return data


def prompt_for_dialog(dialogs: Sequence) -> int | None:
    """Present an indexed list of chats and return the selected index."""

    while True:
        raw = input("Select chat number (blank to cancel): ").strip()
        if not raw:
            return None

        if not raw.isdigit():
            print("Enter a valid number from the list.")
            continue

        idx = int(raw)
        if 1 <= idx <= len(dialogs):
            return idx - 1

        print("Number out of range; try again.")


def sanitize_filename(name: str) -> str:
    """Return a filesystem-friendly name for the chat export."""

    if not name:
        return "chat_export"

    safe = [ch if ch.isalnum() else "_" for ch in name.strip()]
    compact = "".join(safe).strip("_")
    return compact or "chat_export"


def format_message_lines(messages: Iterable) -> list[str]:
    """Transform messages into markdown-friendly lines."""

    lines: list[str] = []

    for message in messages:
        sender = message.sender or message.chat
        display_name = "Unknown"
        if sender is not None:
            pieces = [
                getattr(sender, "title", None),
                getattr(sender, "first_name", None),
            ]
            last_name = getattr(sender, "last_name", None)
            if last_name:
                pieces.append(last_name)
            display_name = next((p for p in pieces if p), "Unknown")

        content = message.message or ""
        if not content:
            if message.media:
                content = "[media]"
            elif message.action:
                content = str(message.action)
            else:
                content = ""

        single_line = " ".join(content.split()) if content else ""

        timestamp = message.date
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        timestamp_str = timestamp.astimezone().isoformat(timespec="seconds")

        lines.append(f"{display_name}: {single_line} ({timestamp_str})")

    return lines


async def main() -> None:
    env = load_env(ENV_FILE)

    try:
        api_id = int(env["TELEGRAM_API_ID"])
        api_hash = env["TELEGRAM_API_HASH"]
    except KeyError as exc:
        missing = exc.args[0]
        raise KeyError(f"Missing {missing} in {ENV_FILE!s}.") from exc

    client = TelegramClient(SESSION_NAME, api_id, api_hash)

    async with client:
        dialogs = await client.get_dialogs()

        if not dialogs:
            print("No chats found.")
            return

        print("Chats you can access:")
        for index, dialog in enumerate(dialogs, start=1):
            entity = dialog.entity
            name = getattr(entity, "title", None) or getattr(entity, "first_name", "(no name)")
            chat_type = (
                "Channel" if dialog.is_channel else "Group" if dialog.is_group else "User"
            )
            print(f"{index}. [{chat_type}] {name}")

        selection = prompt_for_dialog(dialogs)
        if selection is None:
            print("No chat selected; exiting.")
            return

        chosen = dialogs[selection]
        chat_name = getattr(chosen.entity, "title", None) or getattr(
            chosen.entity, "first_name", "chat"
        )

        print(f"Exporting messages from: {chat_name}")

        messages = []
        async for msg in client.iter_messages(chosen.entity):
            messages.append(msg)

        messages.reverse()  # chronological order oldest -> newest

        if not messages:
            print("No messages to export.")
            return

        lines = format_message_lines(messages)

        output_file = Path(f"{sanitize_filename(chat_name)}.md")
        output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

        print(f"Saved {len(lines)} messages to {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
