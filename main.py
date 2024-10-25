import sqlite3
from nicegui import ui

conn = sqlite3.connect("one-api.db")

with ui.header().classes("justify-center"):
    ui.label("Api Tool").classes("text-xl")

cursor = conn.cursor()

cols = [
    {"name": "id", "label": "ID", "field": "id"},
    {"name": "name", "label": "Name", "field": "name"},
    {"name": "url", "label": "BaseUrl", "field": "url"},
    {"name": "key", "label": "ApiKey", "field": "key"},
    {"name": "used", "label": "Used", "field": "used"},
    {"name": "rest", "label": "Rest", "field": "rest"},
    {"name": "speed", "label": "Speed", "field": "speed"},
]

params = {
    "align": "left",
    "sortable": True,
    "headerClasses": "text-primary",
}

with ui.table(rows=[], columns=cols, column_defaults=params).classes("w-full") as table:
    cursor.execute(
        "SELECT id, name, base_url, key, used_quota, balance, response_time FROM channels;"
    )

    for row in cursor.fetchall():
        used = row[4] / 500000
        speed = f"{row[6] / 1000:.2f}s"
        rest = row[5] - used if row[5] else 0
        table.add_row(
            {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "key": row[3],
                "used": used,
                "rest": rest,
                "speed": speed,
            }
        )

ui.run(port=8888)
