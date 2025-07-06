import requests
import datetime

purchase_log = {
    "Seeds": [],
    "Gears": [],
    "Eggs": [],
    "Cosmetics": []
}

def log_purchase(category, item):
    if category in purchase_log:
        purchase_log[category].append(item)

def send_hourly_report(webhook_url):
    if not webhook_url or not any(purchase_log.values()):
        return

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fields = []
    for category, items in purchase_log.items():
        if items:
            fields.append({
                "name": f"{category} Bought",
                "value": ", ".join(items),
                "inline": False
            })

    payload = {
        "embeds": [
            {
                "title": "King Clab's Bot - Hourly Report",
                "description": f"**Hourly Purchase Log**",
                "color": 0x660066,
                "fields": fields,
                "footer": {
                    "text": f"Report generated at {now}"
                }
            }
        ]
    }

    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f"[Webhook Error] {e}")

    # Clear after sending
    for key in purchase_log:
        purchase_log[key] = []

def test_webhook(webhook_url):
    if not webhook_url:
        return False, "No webhook URL provided"
    try:
        response = requests.post(webhook_url, json={
            "embeds": [{
                "title": "King Clab's Bot",
                "description": "Webhook works!",
                "color": 0x660066
            }]
        })
        return (response.status_code in [200, 204]), f"Status: {response.status_code}"
    except Exception as e:
        return False, str(e)
