"""Keep a copy of every bill in a JSON file (default: bills.json)."""

import json
import os
from datetime import datetime


def save_invoice(invoice, path="bills.json"):
    record = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "lines": [
            {"item": item, "qty": qty, "unit_price": price}
            for item, qty, price in invoice.lines
        ],
        "code": invoice.code,
        "total": invoice.calc_total(),
    }
    bills = []
    if os.path.exists(path):
        with open(path) as f:
            bills = json.load(f)
    bills.append(record)
    with open(path, "w") as f:
        json.dump(bills, f, indent=2)
    return record


def load_invoices(path="bills.json"):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)
