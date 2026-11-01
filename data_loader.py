"""
data_loader.py
Bertugas membaca file CSV, memvalidasi kelengkapan dan tipe data setiap baris,
melewati serta menghitung baris yang rusak/tidak terbaca, dan memuatnya ke EcommerceCatalog.
"""

import csv
import os
from models import CSV_FILENAME, REQUIRED_COLUMNS, EcommerceCatalog, OrderRecord


def is_valid_row(row: dict) -> bool:
    """Memeriksa apakah satu baris CSV memiliki semua kolom wajib dan tidak kosong."""
    if not isinstance(row, dict):
        return False
    for col in REQUIRED_COLUMNS:
        if col not in row or row[col] is None or str(row[col]).strip() == "":
            return False
    return True


def parse_row_to_record(row: dict) -> OrderRecord | None:
    """Mengubah satu baris dictionary CSV menjadi objek OrderRecord."""
    if not is_valid_row(row):
        return None
    try:
        quantity = int(str(row["quantity"]).strip())
        unit_price = float(str(row["unit_price"]).strip())
        discount_amount = float(str(row["discount_amount"]).strip())
        gross_sales = float(str(row["gross_sales"]).strip())
        tax_amount = float(str(row["tax_amount"]).strip())
        net_sales = float(str(row["net_sales"]).strip())
        product_cost = float(str(row["product_cost"]).strip())
        profit = float(str(row["profit"]).strip())

        if "shipping_cost" in row and row["shipping_cost"] is not None:
            shipping_str = str(row["shipping_cost"]).strip()
            if shipping_str != "":
                float(shipping_str)
    except (ValueError, TypeError):
        return None

    if quantity <= 0 or unit_price < 0.0 or gross_sales < 0.0 or net_sales < 0.0:
        return None

    return OrderRecord(
        order_id=row["order_id"],
        product_id=row["product_id"],
        product_name=row["product_name"],
        subcategory=row["product_subcategory"],
        quantity=quantity,
        unit_price=unit_price,
        discount_amount=discount_amount,
        gross_sales=gross_sales,
        tax_amount=tax_amount,
        net_sales=net_sales,
        product_cost=product_cost,
        profit=profit,
    )


def load_dataset(filepath: str = CSV_FILENAME) -> EcommerceCatalog:
    """Membaca file CSV dan memuatnya ke dalam EcommerceCatalog."""
    catalog = EcommerceCatalog()
    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(f"File dataset '{filepath}' tidak ditemukan.")

    with open(filepath, mode="r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            return catalog
        for row in reader:
            record = parse_row_to_record(row)
            if record is not None:
                catalog.add_record(record)
            else:
                catalog.skipped_rows += 1
    return catalog