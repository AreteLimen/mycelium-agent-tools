#!/usr/bin/env python3
"""One-shot: read specific messages from the node supergroup via MTProto
(userbot is a member; Bot API getUpdates missed a bot-to-bot message)."""
import asyncio, os, sys
from telethon import TelegramClient

ROOT = os.path.dirname(os.path.abspath(__file__))
SECRET = os.environ.get("USERBOT_ENV") or os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
SESSION = os.environ.get("USERBOT_SESSION") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "userbot")

def creds():
    d = {}
    for line in open(SECRET):
        line = line.strip()
        if "=" in line:
            k, v = line.split("=", 1)
            d[k] = v
    return int(d["ARETE_API_ID"]), d["ARETE_API_HASH"]

async def main():
    api_id, api_hash = creds()
    client = TelegramClient(SESSION, api_id, api_hash)
    await client.start()
    ids = [int(x) for x in sys.argv[1:]]
    msgs = await client.get_messages(-1004301095307, ids=ids)
    for m in msgs:
        if m is None:
            continue
        sender = await m.get_sender()
        uname = getattr(sender, "username", None) or getattr(sender, "first_name", "?")
        print(f"=== id {m.id} | from {uname} | {m.date}")
        print((m.text or "<non-text>")[:2000])
        print()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
