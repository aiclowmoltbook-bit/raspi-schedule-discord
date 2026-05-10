#!/usr/bin/env python3
# list_events.py - List upcoming events from schedule.ics

import re
from datetime import datetime, timedelta
from pathlib import Path

ICS_PATH = Path(__file__).parent / "schedule.ics"

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
    return sorted(events, key=lambda e: e["start"])

def list_upcoming(days=7):
    now = datetime.now()
    limit = now + timedelta(days=days)
    events = [e for e in parse_events() if now <= e["start"] <= limit]

    if not events:
        print("No upcoming events.")
        return

    for e in events:
        print(f"{e['start'].strftime('%Y-%m-%d %H:%M')} – {e['end'].strftime('%H:%M')}")
        print(f"  📝 {e['title']}")
        if e["description"]:
            print(f"  📋 {e['description']}")
        print()

if __name__ == "__main__":
    list_upcoming()
