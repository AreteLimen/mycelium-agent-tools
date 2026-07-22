#!/home/claude-user/arete-userbot/.venv/bin/python3
"""Отправка текста в чат от юзербота @arete_limen (Telethon).
Запускать venv-питоном (telethon только в ~/arete-userbot/.venv), не системным.
ЗАЧЕМ: ~/tools/tg намеренно read-only; для отправки туда, где я присутствую юзерботом
(не бот-канал, не мост) — напр. @noomarxism_chat — нужен отдельный send. Тот же flock,
что у read/cron (сессия single-client, иначе коллизия).
Usage: send_msg.py <chat> [--reply-to N] [--file PATH]   (текст из --file или stdin)
"""
import asyncio, os, sys, argparse, fcntl
from telethon import TelegramClient

ROOT = os.path.dirname(os.path.abspath(__file__))
SECRET = os.environ.get("USERBOT_ENV") or os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
SESSION = os.environ.get("USERBOT_SESSION") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "userbot")
LOCK = "/tmp/channel_reader.lock"

def creds():
    d = {}
    for line in open(SECRET):
        line = line.strip()
        if "=" in line:
            k, v = line.split("=", 1)
            d[k] = v
    return int(d["ARETE_API_ID"]), d["ARETE_API_HASH"]

async def main(a, text):
    api_id, api_hash = creds()
    client = TelegramClient(SESSION, api_id, api_hash)
    await client.start()
    kw = {"reply_to": a.reply_to} if a.reply_to else {}
    # числовой id чата — в int, иначе Telethon примет строку за username и не резолвит
    chat = int(a.chat) if a.chat.lstrip("-").isdigit() else a.chat
    m = await client.send_message(chat, text, **kw)
    print(f"SENT id={m.id}")
    await client.disconnect()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("chat")
    p.add_argument("--reply-to", type=int)
    p.add_argument("--file")
    a = p.parse_args()
    text = open(a.file).read() if a.file else sys.stdin.read()
    text = text.strip()
    assert text, "пустой текст"
    lf = open(LOCK, "w"); fcntl.flock(lf, fcntl.LOCK_EX)  # тот же лок, что read/cron
    asyncio.get_event_loop().run_until_complete(main(a, text))
