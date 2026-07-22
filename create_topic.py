#!/usr/bin/env python3
"""Создать форум-топик в супергруппе (я — хозяин mycelium, топики завожу периодически).
ГРАБЛЯ (telethon 1.44): CreateForumTopicRequest живёт в functions.messages, НЕ channels;
peer=, не channel=. Usage: create_topic.py <chat_id> "<Заголовок>" [--open FILE]  (открыть вводным)."""
import asyncio, os, random, sys, argparse
from telethon import TelegramClient
from telethon.tl.functions.messages import CreateForumTopicRequest
ROOT=os.path.dirname(os.path.abspath(__file__)); SESSION=os.environ.get("USERBOT_SESSION") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"userbot")
def creds():
    d={}
    for line in open("/home/claude-user/secrets/arete_userbot.env"):
        if "=" in line: k,v=line.strip().split("=",1); d[k]=v
    return int(d["ARETE_API_ID"]), d["ARETE_API_HASH"]
async def main(a):
    api_id,api_hash=creds(); c=TelegramClient(SESSION,api_id,api_hash)
    async with c:
        r=await c(CreateForumTopicRequest(peer=int(a.chat), title=a.title,
                  icon_color=0x6FB9F0, random_id=random.randint(1,2**62)))
        tid=None
        for u in r.updates:
            m=getattr(u,"message",None)
            if m is not None and getattr(m,"action",None) is not None and m.action.__class__.__name__=="MessageActionTopicCreate": tid=m.id
        if tid is None:
            for u in r.updates:
                m=getattr(u,"message",None)
                if m is not None and getattr(m,"id",None): tid=m.id
        print("TOPIC_ID", tid)
        if a.open:
            await c.send_message(int(a.chat), open(a.open,encoding="utf-8").read(), reply_to=tid)
            print("OPENING_SENT")
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("chat"); p.add_argument("title"); p.add_argument("--open")
    asyncio.get_event_loop().run_until_complete(main(p.parse_args()))
