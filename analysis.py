"""
analysis.py
Berisi fungsi-fungsi analisis data, pengurutan manual, pemotongan list, pencarian, dan filter.
"""

from models import EcommerceCatalog, OrderRecord
from text_utils import clean_text


def manual_sort_dicts(items: list[dict], key_name: str, descending: bool = True) -> list[dict]:
    """Mengurutkan list dictionary menggunakan Selection Sort (for loop bersarang)."""
    result = list(items)
    n = len(result)
    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            val_j = result[j].get(key_name, 0)
            val_target = result[target_idx].get(key_name, 0)
            if descending and val_j > val_target:
                target_idx = j
            elif not descending and val_j < val_target:
                target_idx = j
        if target_idx != i:
            temp = result[i]
            result[i] = result[target_idx]
            result[target_idx] = temp
    return result


def get_top_profitable_products(catalog: EcommerceCatalog, top_n: int = 10) -> list[dict]:
    """Target 1: Mengambil N produk dengan total keuntungan (profit) tertinggi."""
    if not isinstance(catalog, EcommerceCatalog) or top_n <= 0:
        return []
    product_map: dict[str, dict] = {}
    for rec in catalog.records:
        pid = rec.product_id
        if pid not in product_map:
            product_map[pid] = {
                "product_id": pid,
                "product_name": rec.product_name,
                "brand": rec.brand,
                "subcategory": rec.subcategory,
                "total_quantity": 0,
                "total_net_sales": 0.0,
                "total_profit": 0.0,
                "order_count": 0,
            }
        product_map[pid]["total_quantity"] += rec.quantity
        product_map[pid]["total_net_sales"] += rec.net_sales
        product_map[pid]["total_profit"] += rec.profit
        product_map[pid]["order_count"] += 1

    product_list: list[dict] = []
    for item in product_map.values():
        if item["total_net_sales"] > 0:
            item["profit_margin"] = (item["total_profit"] / item["total_net_sales"]) * 100.0
        else:
            item["profit_margin"] = 0.0
        product_list.append(item)

    sorted_products = manual_sort_dicts(product_list, key_name="total_profit", descending=True)
    return sorted_products[:top_n]


def get_category_sales_contribution(catalog: EcommerceCatalog, top_n: int = 10) -> list[dict]:
    """Target 2: Menghitung kontribusi penjualan setiap subkategori terhadap total penjualan."""
    if not isinstance(catalog, EcommerceCatalog) or top_n <= 0:
        return []
    grand_total_sales = catalog.get_total_net_sales()
    category_map: dict[str, dict] = {}
    for rec in catalog.records:
        cat = rec.subcategory
        if cat not in category_map:
            category_map[cat] = {
                "subcategory": cat,
                "order_count": 0,
                "total_quantity": 0,
                "total_net_sales": 0.0,
                "total_profit": 0.0,
            }
        category_map[cat]["order_count"] += 1
        category_map[cat]["total_quantity"] += rec.quantity
        category_map[cat]["total_net_sales"] += rec.net_sales
        category_map[cat]["total_profit"] += rec.profit

    category_list: list[dict] = []
    for item in category_map.values():
        if grand_total_sales > 0:
            item["sales_contribution_pct"] = (item["total_net_sales"] / grand_total_sales) * 100.0
        else:
            item["sales_contribution_pct"] = 0.0

        if item["order_count"] > 0:
            item["avg_order_sales"] = item["total_net_sales"] / item["order_count"]
        else:
            item["avg_order_sales"] = 0.0

        category_list.append(item)

    sorted_categories = manual_sort_dicts(category_list, key_name="total_net_sales", descending=True)
    return sorted_categories[:top_n]


def get_top_performing_brands(catalog: EcommerceCatalog, sort_by: str = "total_profit", top_n: int = 10) -> list[dict]:
    """Target 3: Mengevaluasi merek (brand) dengan kinerja terbaik."""
    if not isinstance(catalog, EcommerceCatalog) or top_n <= 0:
        return []
    valid_keys = ["total_profit", "total_net_sales", "profit_margin", "total_quantity"]
    if sort_by not in valid_keys:
        sort_by = "total_profit"

    brand_map: dict[str, dict] = {}
    for rec in catalog.records:
        b_name = rec.brand
        if b_name not in brand_map:
            brand_map[b_name] = {
                "brand": b_name,
                "order_count": 0,
                "total_quantity": 0,
                "total_net_sales": 0.0,
                "total_profit": 0.0,
            }
        brand_map[b_name]["order_count"] += 1
        brand_map[b_name]["total_quantity"] += rec.quantity
        brand_map[b_name]["total_net_sales"] += rec.net_sales
        brand_map[b_name]["total_profit"] += rec.profit

    brand_list: list[dict] = []
    for item in brand_map.values():
        if item["total_net_sales"] > 0:
            item["profit_margin"] = (item["total_profit"] / item["total_net_sales"]) * 100.0
        else:
            item["profit_margin"] = 0.0

        if item["order_count"] > 0:
            item["avg_profit_per_order"] = item["total_profit"] / item["order_count"]
        else:
            item["avg_profit_per_order"] = 0.0

        if item["total_profit"] >= 1500.0 and item["profit_margin"] >= 20.0:
            item["brand_status"] = "Sangat Unggul"
        elif item["total_profit"] >= 500.0 and item["profit_margin"] >= 10.0:
            item["brand_status"] = "Baik"
        elif item["total_profit"] > 0.0:
            item["brand_status"] = "Standar"
        else:
            item["brand_status"] = "Evaluasi (Rugi)"

        brand_list.append(item)

    sorted_brands = manual_sort_dicts(brand_list, key_name=sort_by, descending=True)
    return sorted_brands[:top_n]


def search_records(catalog: EcommerceCatalog, keyword: str) -> list[OrderRecord]:
    """Mencari transaksi berdasarkan kata kunci (mengabaikan huruf kapital & tanda baca)."""
    if not isinstance(catalog, EcommerceCatalog):
        return []
    clean_kw = clean_text(keyword)
    if not clean_kw:
        return []
    matched: list[OrderRecord] = []
    for rec in catalog.records:
        if (
            clean_kw in clean_text(rec.product_name)
            or clean_kw in clean_text(rec.brand)
            or clean_kw in clean_text(rec.subcategory)
            or clean_kw in clean_text(rec.product_id)
        ):
            matched.append(rec)
    return matched


def filter_records_by_criteria(
    catalog: EcommerceCatalog,
    min_profit: float = 0.0,
    only_profitable: bool = True,
    subcategory_query: str = "",
) -> list[OrderRecord]:
    """Menyaring transaksi berdasarkan batas profit dan subkategori."""
    if not isinstance(catalog, EcommerceCatalog):
        return []
    clean_cat = clean_text(subcategory_query)
    filtered: list[OrderRecord] = []
    for rec in catalog.records:
        if only_profitable and not rec.is_profitable:
            continue
        if rec.profit < min_profit:
            continue
        if clean_cat != "" and clean_cat not in clean_text(rec.subcategory):
            continue
        filtered.append(rec)
    return filtered