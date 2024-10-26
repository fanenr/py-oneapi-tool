import sqlite3
from nicegui import ui

conn = sqlite3.connect("one-api.db")
conn.row_factory = sqlite3.Row

with ui.header().classes("justify-center"):
    ui.label("OneAPI Tool").classes("text-xl text-bold")

cursor = conn.cursor()
rows = {}

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
    "rows": [],
    "columns": cols,
    "selection": "single",
    "column_defaults": {
        "align": "left",
        "sortable": True,
        "headerClasses": "text-primary",
    },
}

with ui.table(**params).props("flat bordered").classes("w-full") as table:
    cursor.execute("SELECT * FROM channels;")

    for row in cursor.fetchall():
        rows[row["id"]] = row
        used = row["used_quota"] / 500000
        speed = f"{row['response_time'] / 1000:.2f}s"
        rest = row["balance"] - used if row["balance"] else 0

        table.add_row(
            {
                "used": used,
                "rest": rest,
                "speed": speed,
                "id": row["id"],
                "key": row["key"],
                "name": row["name"],
                "url": row["base_url"],
            }
        )


with ui.card().props("flat bordered").classes("w-full"):
    ui.label("Channel Information").classes("text-base text-bold")

    with ui.row().classes("w-full justify-center"):
        with ui.column():
            ui.label("Channel Nmae")
            edit_name = ui.input().props("outlined dense")
        with ui.column():
            ui.label("Base URL")
            edit_url = ui.input().props("outlined dense")
        with ui.column():
            ui.label("API Key")
            edit_key = ui.input().props("outlined dense")

    with ui.row().classes("w-full justify-center"):
        with ui.column().classes("w-1/3"):
            ui.label("Models")
            edit_models = ui.textarea().props("outlined dense").classes("w-full")
        with ui.column().classes("w-1/3"):
            ui.label("Model Mapping")
            edit_mapping = ui.textarea().props("outlined dense").classes("w-full")


def on_select(ev):
    if len(selection := ev.selection) <= 0:
        edit_mapping.set_value(None)
        edit_models.set_value(None)
        edit_name.set_value(None)
        edit_url.set_value(None)
        edit_key.set_value(None)
        return

    row = rows[selection[0]["id"]]

    edit_key.set_value(row["key"])
    edit_name.set_value(row["name"])
    edit_url.set_value(row["base_url"])

    edit_models.set_value(row["models"])
    edit_mapping.set_value(row["model_mapping"])


table.on_select(on_select)

ui.run(port=8888)
