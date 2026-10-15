# db.py
import sqlite3
from pathlib import Path
import uuid

UPLOAD_DIR = Path(__file__).parent / "data" / "uploads"
DB_PATH = Path(__file__).parent / "data" / "receipts.db"


def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS receipts (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            store         TEXT,
            purchase_date TEXT,   -- 'YYYY-MM-DD'
            total         REAL,
            fees          REAL,
            discounts     REAL DEFAULT 0,
            image_path    TEXT,
            uploaded_at   TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS items (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER REFERENCES receipts(id),
            name       TEXT,
            quantity   INTEGER,
            price      REAL
        );
        """)
        
def save_image(image_bytes, original_name):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ext = Path(original_name).suffix or ".png"     
    path = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
    path.write_bytes(image_bytes)
    return str(path)

def save_receipt(data, image_path):
    with get_conn() as conn:
        cur = conn.cursor()

        # 1. One row for the receipt
        cur.execute(
            """INSERT INTO receipts (store, purchase_date, total, fees, discounts, image_path)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (data["store"], data["purchase_date"], data["total"], data["fees"], data["discounts"], image_path),
        )
        receipt_id = cur.lastrowid   # the ID SQLite just generated

        # 2. One row per item, linked by receipt_id
        for item in data["items"]:
            cur.execute(
                """INSERT INTO items (receipt_id, name, quantity, price)
                   VALUES (?, ?, ?, ?)""",
                (receipt_id, item["name"], item["quantity"], item["price"]),
            )

    return receipt_id