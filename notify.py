#!/usr/bin/env python3
# notify.py - Send Discord notifications 60 and 10 minutes before events
# Designed to be run every minute via cron.

import re
import json
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
ICS_PATH = BASE_DIR / "schedule.ics"
CONFIG_PATH = BASE_DIR / "config.json"

NOTIFY_MINUTES = [60, 10]

def get_webhook_url():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return config["discord_webhook_url"]

def parse_events():
    content = ICS_PATH.read_text(encoding="utf-8")
    events = []
    for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", content, re.DOTALL):
        def get(key, b=block):
            m = re.search(rf"^{key}:(.+)$", b, re.MULTILINE)
            return m.group(1).strip() if m else ""
        try:
            dt_start = datetime.strptime(get("DTSTART"), "%Y%m%dT%H%M%S")
            dt_end = datetime.strptime(get("DTEND"), "%Y%m%dT%H%M%S")
            events.append({
                "start": dt_start,
                "end": dt_end,
                "title": get("SUMMARY"),
                "description": get("DESCRIPTION").replace("\\n", "\n"),
            })
        except ValueError:
            continue
    return events

def send_discord(webhook_url, message):
    payload = json.dumps({"content": message}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )
    urllib.request.urlopen(req, timeout=10)

def check_and_notify():
    now = datetime.now().replace(second=0, microsecond=0)
    webhook_url = get_webhook_url()
    events = parse_events()

    for event in events:
        for minutes in NOTIFY_MINUTES:
            notify_at = event["start"] - timedelta(minutes=minutes)
            if now == notify_at:
                label = "1 hour" if minutes == 60 else f"{minutes} minutes"
                desc = f"\n📋 {event['description']}" if event["description"] else ""
                msg = (
                    f"⏰ **Upcoming in {label}**\n"
                    f"🕐 {event['start'].strftime('%H:%M')} – {event['end'].strftime('%H:%M')}\n"
                    f"📝 {event['title']}"
                    f"{desc}"
                )
                try:
                    send_discord(webhook_url, msg)
                    print(f"[OK] Notified: {event['title']} ({label} before)")
                except Exception as e:
                    print(f"[ERROR] Failed to send notification: {e}")

if __name__ == "__main__":
    check_and_notify()
