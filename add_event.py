#!/usr/bin/env python3
# add_event.py - Add an event to schedule.ics

import uuid
from datetime import datetime
from pathlib import Path

ICS_PATH = Path(__file__).parent / "schedule.ics"

def add_event(date, start_time, end_time, title, description=""):
    """
    Add an event to the schedule.
    date: "2026-05-15"
    start_time: "14:00"
    end_time: "15:30"
    title: "Meeting title"
    description: "Optional notes (multi-line supported)"
    """
    uid = str(uuid.uuid4())
    dt_start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    dt_end = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

    desc_escaped = description.replace("\n", "\\n")

    new_event = (
        f"BEGIN:VEVENT\n"
        f"UID:{uid}\n"
        f"DTSTART:{dt_start.strftime('%Y%m%dT%H%M%S')}\n"
        f"DTEND:{dt_end.strftime('%Y%m%dT%H%M%S')}\n"
        f"SUMMARY:{title}\n"
        f"DESCRIPTION:{desc_escaped}\n"
        f"END:VEVENT\n"
    )

    content = ICS_PATH.read_text(encoding="utf-8")
    updated = content.replace("END:VCALENDAR", new_event + "END:VCALENDAR")
    ICS_PATH.write_text(updated, encoding="utf-8")
    print(f"[OK] Event added: {title} ({date} {start_time}–{end_time})")


if __name__ == "__main__":
    # Example usage
    add_event(
        date="2026-05-15",
        start_time="14:00",
        end_time="15:30",
        title="Sample Meeting",
        description="Agenda item 1\nAgenda item 2"
    )
