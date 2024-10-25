import sqlite3
from nicegui import ui

conn = sqlite3.connect("one-api.db")

with ui.header().classes("justify-center"):
    ui.label("Api Tool").classes("text-xl")

with ui.row().classes("w-full"):
    cursor = conn.cursor()

    with ui.list().props("bordered separator"):
        ui.item_label("Tables").props("header").classes("text-bold")
        ui.separator()

        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")

        for row in cursor.fetchall():
            with ui.item().classes("items-center"):
                ui.item_label(row[0])

    cols = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "name", "label": "Name", "field": "name"},
        {"name": "url", "label": "BaseUrl", "field": "url"},
        {"name": "key", "label": "ApiKey", "field": "key"},
        {"name": "speed", "label": "Speed", "field": "speed"},
    ]
    params = {
        "align": "left",
        "sortable": True,
        "headerClasses": "text-primary",
    }
    with ui.table(rows=[], columns=cols, column_defaults=params).classes(
        "flex-1"
    ) as table:
        cursor.execute("SELECT id, name, base_url, key, response_time FROM channels;")

        for row in cursor.fetchall():
            speed = f"{row[4] / 1000:.2f}s"
            table.add_row(
                {
                    "id": row[0],
                    "name": row[1],
                    "url": row[2],
                    "key": row[3],
                    "speed": speed,
                }
            )

    cursor.close()

ui.run(port=8888)
