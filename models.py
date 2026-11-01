"""
models.py
Berisi konstanta global serta definisi Class OrderRecord dan EcommerceCatalog (Bonus OOP).
"""

from text_utils import extract_brand, format_truncate

# ==========================================
# KONSTANTA (Ditulis dengan huruf kapital)
# ==========================================
CSV_FILENAME = "dataset_ecommerce.csv"
HIGH_MARGIN_THRESHOLD = 30.0
LOW_MARGIN_THRESHOLD = 10.0

REQUIRED_COLUMNS = [
    "order_id",
    "product_id",
    "product_name",
    "product_subcategory",
    "quantity",
    "unit_price",
    "discount_amount",
    "gross_sales",
    "tax_amount",
    "net_sales",
    "product_cost",
    "profit",
]


# ==========================================
# BONUS OOP - CLASS 1: Menyimpan Setiap Record
# ==========================================
class OrderRecord:
    """Merepresentasikan satu baris transaksi produk dari file CSV."""

    def __init__(
        self,
        order_id: str,
        product_id: str,
        product_name: str,
        subcategory: str,
        quantity: int,
        unit_price: float,
        discount_amount: float,
        gross_sales: float,
        tax_amount: float,
        net_sales: float,
        product_cost: float,
        profit: float,
    ):
        # Atribut teks (str) dan pemanggilan fungsi pembantu dari text_utils
        self.order_id = str(order_id).strip()
        self.product_id = str(product_id).strip()
        self.product_name = str(product_name).strip()
        self.subcategory = str(subcategory).strip()
        self.brand = extract_brand(self.product_name, self.subcategory)

        # Atribut numerik (int dan float)
        self.quantity = int(quantity)
        self.unit_price = float(unit_price)
        self.discount_amount = float(discount_amount)
        self.gross_sales = float(gross_sales)
        self.tax_amount = float(tax_amount)
        self.net_sales = float(net_sales)
        self.product_cost = float(product_cost)
        self.profit = float(profit)

        # Tipe data boolean (bool) menggunakan operator relasional
        self.is_profitable = self.profit > 0.0

        # Operator aritmatika: menghitung 2 nilai turunan (margin profit % dan rasio diskon %)
        # Dilengkapi proteksi pembagian dengan nol (ZeroDivisionError)
        if self.net_sales > 0:
            self.profit_margin = (self.profit / self.net_sales) * 100.0
        else:
            self.profit_margin = 0.0

        if self.gross_sales > 0:
            self.discount_rate = (self.discount_amount / self.gross_sales) * 100.0
        else:
            self.discount_rate = 0.0

        # Pernyataan bersyarat (if-elif-else minimal 3 hasil) + operator logika (and, not)
        if not self.is_profitable:
            self.performance_tier = "Rugi (Loss)"
        elif self.profit_margin >= HIGH_MARGIN_THRESHOLD and self.quantity >= 1:
            self.performance_tier = "Margin Tinggi"
        elif self.profit_margin >= LOW_MARGIN_THRESHOLD:
            self.performance_tier = "Margin Sedang"
        else:
            self.performance_tier = "Margin Rendah"

    def __str__(self) -> str:
        """Mengembalikan representasi string terformat dengan kolom sejajar."""
        short_name = format_truncate(self.product_name, 30)
        return (
            f"{self.product_id:<12} | {self.brand:<16} | {short_name:<30} | "
            f"{self.subcategory:<18} | {self.quantity:>4} | "
            f"${self.net_sales:>10.2f} | ${self.profit:>9.2f} | {self.profit_margin:>6.1f}%"
        )


# ==========================================
# BONUS OOP - CLASS 2: Menyimpan Daftar Record
# ==========================================
class EcommerceCatalog:
    """Menyimpan koleksi list dari objek OrderRecord dan metadata pemuatan CSV."""

    def __init__(self):
        self.records: list[OrderRecord] = []
        self.skipped_rows: int = 0

    def add_record(self, record: OrderRecord) -> None:
        """Menambahkan satu objek OrderRecord ke dalam list records."""
        if isinstance(record, OrderRecord):
            self.records.append(record)

    def total_records(self) -> int:
        """Mengembalikan jumlah total record yang berhasil dimuat."""
        return len(self.records)

    def get_total_net_sales(self) -> float:
        """Menghitung total keseluruhan net_sales menggunakan perulangan for."""
        total = 0.0
        for rec in self.records:
            total += rec.net_sales
        return total

    def get_total_profit(self) -> float:
        """Menghitung total keseluruhan profit menggunakan perulangan for."""
        total = 0.0
        for rec in self.records:
            total += rec.profit
        return total

    def __str__(self) -> str:
        return (
            f"EcommerceCatalog(Dimuat: {self.total_records()} baris, "
            f"Dilewati: {self.skipped_rows} baris, "
            f"Total Penjualan Bersih: ${self.get_total_net_sales():,.2f})"
        )