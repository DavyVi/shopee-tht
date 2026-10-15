from db import get_conn

def get_items_by_date(date: str) -> list:
    """All items bought on a given date (YYYY-MM-DD)."""
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT i.name, i.quantity, i.price, r.store
               FROM items i JOIN receipts r ON i.receipt_id = r.id
               WHERE r.purchase_date = ?""",
            (date,),
        ).fetchall()
    return [{"item": n, "quantity": q, "price": p, "store": s} for n, q, p, s in rows]

def get_total_by_date(date: str) -> dict:
    """Total spent on a given date (YYYY-MM-DD)."""
    with get_conn() as conn:
        total = conn.execute(
            """SELECT SUM(total) FROM receipts WHERE purchase_date = ?""",
            (date,),
        ).fetchone()[0]
    return {"total": total} if total is not None else {"total": 0.0}

def find_stores_by_item(item_keyword: str, start_date: str, end_date: str) -> list:
    """Find all stores where a specific item was purchased within a date range."""
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT DISTINCT r.store, r.purchase_date
               FROM items i JOIN receipts r ON i.receipt_id = r.id
               WHERE i.name LIKE ? AND r.purchase_date BETWEEN ? AND ?""",
            (f"%{item_keyword}%", start_date, end_date),
        ).fetchall()
    return [{"store": s, "purchase_date": d} for s, d in rows]

TOOLS = {
    "get_items_by_date": get_items_by_date,
    "get_total_by_date": get_total_by_date,
    "find_stores_by_item": find_stores_by_item,
}

DECLARATIONS = [
    {
        "type": "function",
        "name": "get_items_by_date",
        "description": "Get all food items purchased on a specific date.",
        "parameters": {
            "type": "object",
            "properties": {"date": {"type": "string", "description": "Date in YYYY-MM-DD"}},
            "required": ["date"],
        },
    },
    {
        "type": "function",
        "name": "get_total_by_date",
        "description": "Get the total amount spent on a specific date.",
        "parameters": {
            "type": "object",
            "properties": {"date": {"type": "string", "description": "Date in YYYY-MM-DD"}},
            "required": ["date"],
        },
    },
    {
        "type": "function",
        "name": "find_stores_by_item",
        "description": "Find all stores where a specific item was purchased within a date range.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_keyword": {"type": "string", "description": "Keyword to search for in item names."},
                "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD."},
                "end_date": {"type": "string", "description": "End date in YYYY-MM-DD."},
            },
            "required": ["item_keyword", "start_date", "end_date"],
        },
    },
]