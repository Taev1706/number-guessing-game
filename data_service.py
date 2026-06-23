import csv
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "records.csv")
FIELDNAMES = ["name", "attempts"]


def _ensure_file():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_all() -> list:
    _ensure_file()
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_all(rows: list):
    _ensure_file()
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def add_record(name: str, attempts: int) -> dict:
    if not name or not name.strip():
        raise ValueError("Имя игрока не может быть пустым.")
    if not isinstance(attempts, int) or attempts < 1:
        raise ValueError("Количество попыток должно быть целым положительным числом.")

    row = {"name": name.strip(), "attempts": attempts}
    rows = load_all()
    rows.append(row)
    save_all(rows)
    return row


def get_all_records() -> list:
    return load_all()


def clear_all():
    save_all([])