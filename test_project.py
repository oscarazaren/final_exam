# unitest 
"""
test_project.py
Modul pengujian unit (unit testing) menggunakan pustaka standar unittest.
Menguji input normal, kasus ekstrem (edge cases), dan input buruk.
"""

import unittest
from analysis import (
    manual_sort_dicts,
    get_top_profitable_products,
    search_records,
)
from data_loader import is_valid_row, parse_row_to_record
from models import EcommerceCatalog, OrderRecord
from text_utils import clean_text, extract_brand, format_truncate


class TestEcommerceProject(unittest.TestCase):
    """Kelas pengujian unit untuk seluruh modul proyek e-commerce."""

    def setUp(self):
        """Menyiapkan data sampel dummy sebelum setiap pengujian dijalankan."""
        self.sample_row = {
            "order_id": "ORD-123456",
            "product_id": "PROD-0001",
            "product_name": "Garmin Fast tactical GPS Smart Watches",
            "product_subcategory": "Smart Watches",
            "quantity": "2",
            "unit_price": "150.00",
            "discount_amount": "20.00",
            "gross_sales": "300.00",
            "tax_amount": "15.00",
            "net_sales": "295.00",
            "product_cost": "100.00",
            "profit": "195.00",
        }

    def test_text_utils_clean_and_brand(self):
        """Test 1: Menguji fungsi pembersihan string dan ekstraksi merek (normal & edge case)."""
        # Uji normal clean_text
        raw = "  Sony-Interactive  'Entertainment' & Media  "
        cleaned = clean_text(raw)
        self.assertEqual(cleaned, "sony interactive entertainment and media")

        # Uji extract_brand normal
        brand = extract_brand("Garmin Fast tactical GPS Smart Watches", "Smart Watches")
        self.assertEqual(brand, "Garmin")

        # Uji edge case string kosong atau bukan string
        self.assertEqual(clean_text(None), "")
        self.assertEqual(extract_brand(""), "Unknown")
        self.assertEqual(format_truncate("Short", 2), "Sh")

    def test_order_record_creation_and_zero_division(self):
        """Test 2: Menguji pembuatan OrderRecord dan proteksi pembagian dengan nol (edge case)."""
        # Pembuatan record normal
        rec = OrderRecord(
            order_id="ORD-001",
            product_id="PROD-99",
            product_name="Nike Air Shoes",
            subcategory="Shoes",
            quantity=1,
            unit_price=100.0,
            discount_amount=0.0,
            gross_sales=100.0,
            tax_amount=5.0,
            net_sales=100.0,
            product_cost=50.0,
            profit=50.0,
        )
        self.assertTrue(rec.is_profitable)
        self.assertEqual(rec.brand, "Nike")
        self.assertAlmostEqual(rec.profit_margin, 50.0)

        # Uji edge case: net_sales = 0 (mencegah pembagian dengan nol)
        rec_zero = OrderRecord(
            order_id="ORD-002",
            product_id="PROD-00",
            product_name="Test Item",
            subcategory="Test",
            quantity=1,
            unit_price=0.0,
            discount_amount=0.0,
            gross_sales=0.0,
            tax_amount=0.0,
            net_sales=0.0,
            product_cost=10.0,
            profit=-10.0,
        )
        self.assertEqual(rec_zero.profit_margin, 0.0)
        self.assertEqual(rec_zero.discount_rate, 0.0)

    def test_data_loader_validation_and_bad_input(self):
        """Test 3: Menguji validasi baris CSV dengan input buruk (bad input)."""
        # Baris lengkap dan valid
        self.assertTrue(is_valid_row(self.sample_row))

        # Baris dengan input buruk: kolom wajib kosong / hilang
        bad_row = dict(self.sample_row)
        bad_row["unit_price"] = ""
        self.assertFalse(is_valid_row(bad_row))

        # Parse row dengan angka rusak (bad input)
        bad_parse_row = dict(self.sample_row)
        bad_parse_row["quantity"] = "bukan_angka"
        parsed_result = parse_row_to_record(bad_parse_row)
        self.assertIsNone(parsed_result)

    def test_manual_sorting_algorithm(self):
        """Test 4: Menguji algoritma pengurutan manual (Selection Sort) tanpa sorted()."""
        dummy_items = [
            {"name": "A", "score": 10},
            {"name": "B", "score": 50},
            {"name": "C", "score": 30},
        ]
        # Urutkan dari besar ke kecil (descending)
        sorted_desc = manual_sort_dicts(dummy_items, key_name="score", descending=True)
        self.assertEqual(sorted_desc[0]["score"], 50)
        self.assertEqual(sorted_desc[2]["score"], 10)

        # Urutkan dari kecil ke besar (ascending)
        sorted_asc = manual_sort_dicts(dummy_items, key_name="score", descending=False)
        self.assertEqual(sorted_asc[0]["score"], 10)
        self.assertEqual(sorted_asc[2]["score"], 50)

    def test_catalog_aggregation_and_search(self):
        """Test 5: Menguji agregasi katalog dan fitur pencarian."""
        catalog = EcommerceCatalog()
        rec1 = OrderRecord(
            "ORD-1", "PROD-A", "Sony Bravia TVs", "TVs", 1, 500.0, 0.0, 500.0, 10.0, 500.0, 300.0, 200.0
        )
        rec2 = OrderRecord(
            "ORD-2", "PROD-B", "Samsung Galaxy Smartphones", "Smartphones", 2, 300.0, 0.0, 600.0, 10.0, 600.0, 400.0, 200.0
        )
        catalog.add_record(rec1)
        catalog.add_record(rec2)

        self.assertEqual(catalog.total_records(), 2)
        self.assertEqual(catalog.get_total_net_sales(), 1100.0)

        # Uji pencarian produk
        search_res = search_records(catalog, "bravia")
        self.assertEqual(len(search_res), 1)
        self.assertEqual(search_res[0].product_id, "PROD-A")

        # Uji top profitable products
        top_prod = get_top_profitable_products(catalog, top_n=1)
        self.assertEqual(len(top_prod), 1)


if __name__ == "__main__":
    unittest.main()