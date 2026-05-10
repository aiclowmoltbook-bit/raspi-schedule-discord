# raspi-schedule-discord

A lightweight schedule manager for Raspberry Pi that sends Discord notifications 60 and 10 minutes before your events. Stores events in iCal format (.ics), fully offline-capable, and easy to set up with cron. Perfect for personal or small-team use in a closed environment.

---

## Features

- 📅 Store events in standard iCal (`.ics`) format
- ⏰ Discord notifications 60 min and 10 min before each event
- 🔒 Runs entirely on your local machine — no cloud dependency
- 🐍 Pure Python 3, no external libraries required
- 🔁 Cron-based — set it and forget it

---

## File Structure

```
raspi-schedule-discord/
├── schedule.ics          # Event data (iCal format)
├── add_event.py          # Add a new event
├── list_events.py        # List upcoming events (next 7 days)
├── notify.py             # Discord notifier (run via cron every minute)
├── config.json           # Your Discord webhook URL (not committed)
├── config.example.json   # Template — copy this to config.json
└── notify.log            # Notification log (created automatically)
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/aiclowmoltbook-bit/raspi-schedule-discord.git
cd raspi-schedule-discord
```

### 2. Configure Discord Webhook

Copy the example config and add your webhook URL:

```bash
cp config.example.json config.json
```

Edit `config.json`:

```json
{
  "discord_webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
}
```

> To create a webhook: Discord channel → Edit Channel → Integrations → Webhooks → New Webhook

### 3. Set up cron (check every minute)

```bash
crontab -e
```

Add this line (adjust the path to match your clone location):

```cron
* * * * * /usr/bin/python3 /home/pi/raspi-schedule-discord/notify.py >> /home/pi/raspi-schedule-discord/notify.log 2>&1
```

---

## Usage

### Add an event

Edit `add_event.py` and run it:

```python
add_event(
    date="2026-05-15",
    start_time="14:00",
    end_time="15:30",
    title="Team Meeting",
    description="Discuss Q2 goals.\nBring the report."
)
```

```bash
python3 add_event.py
```

### List upcoming events (next 7 days)

```bash
python3 list_events.py
```

### Example Discord notification

```
⏰ Upcoming in 1 hour
🕐 14:00 – 15:30
📝 Team Meeting
📋 Discuss Q2 goals.
Bring the report.
```

---

## Requirements

- Python 3.6+
- Raspberry Pi (tested on Raspberry Pi 400, aarch64)
- A Discord server with a configured Webhook

---

## License

MIT
