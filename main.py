"""
main.py
Titik masuk utama aplikasi (entry point).
Menangani pemuatan awal dataset, menu interaktif (while loop), validasi input pengguna,
dan pencetakan hasil analisis dalam tabel dengan kolom yang sejajar (f-string).
"""

from analysis import (
    filter_records_by_criteria,
    get_category_sales_contribution,
    get_top_performing_brands,
    get_top_profitable_products,
    search_records,
)
from data_loader import load_dataset
from models import CSV_FILENAME, EcommerceCatalog, OrderRecord
from text_utils import format_truncate

# Konstanta untuk garis pembatas tabel
TABLE_DIVIDER = "=" * 98
ROW_DIVIDER = "-" * 98


# ==========================================
# FUNGSI VALIDASI INPUT (Dalam Loop Anti-Crash)
# ==========================================
def prompt_int(prompt_msg: str, min_val: int = 1, max_val: int = 100) -> int:
    """
    Meminta input bilangan bulat (int) dari pengguna di dalam perulangan while.
    Memberikan pesan jelas jika input salah dan meminta ulang tanpa crash.
    """
    while True:
        raw_input = input(prompt_msg).strip()
        try:
            value = int(raw_input)
            if min_val <= value <= max_val:
                return value
            print(
                f"  [!] Input di luar batas. Masukkan angka bulat antara {min_val} hingga {max_val}."
            )
        except ValueError:
            print(
                f"  [!] Input '{raw_input}' tidak valid. Harap masukkan angka bulat (contoh: 5 atau 10)."
            )


def prompt_float(prompt_msg: str, min_val: float = -100000.0) -> float:
    """
    Meminta input angka desimal (float) dari pengguna di dalam perulangan while.
    """
    while True:
        raw_input = input(prompt_msg).strip()
        try:
            value = float(raw_input)
            if value >= min_val:
                return value
            print(f"  [!] Nilai tidak boleh kurang dari {min_val}.")
        except ValueError:
            print(
                f"  [!] Input '{raw_input}' bukan angka valid. Gunakan titik untuk desimal (contoh: 100.5)."
            )


def prompt_yes_no(prompt_msg: str) -> bool:
    """
    Meminta konfirmasi Ya/Tidak (y/n) dan mengembalikan nilai boolean (True/False).
    """
    while True:
        ans = input(prompt_msg).strip().lower()
        if ans in ("y", "ya", "yes"):
            return True
        if ans in ("n", "tidak", "no"):
            return False
        print("  [!] Pilihan tidak dikenali. Ketik 'y' (Ya) atau 'n' (Tidak).")


# ==========================================
# FUNGSI PENCETAKAN TABEL (Kolom Sejajar)
# ==========================================
def display_top_products(catalog: EcommerceCatalog) -> None:
    """Menampilkan Target 1: Produk dengan keuntungan (profit) tertinggi."""
    print("\n--- [FITUR 1] PRODUK DENGAN KEUNTUNGAN TERTINGGI ---")
    top_n = prompt_int("Masukkan jumlah produk teratas yang ingin ditampilkan (1-50): ", 1, 50)
    results = get_top_profitable_products(catalog, top_n=top_n)

    if not results:
        print("  Tidak ada data produk untuk ditampilkan.")
        return

    print("\n" + TABLE_DIVIDER)
    print(
        f"{'No':<4} | {'ID Produk':<11} | {'Merek':<15} | {'Nama Produk':<26} | "
        f"{'Qty':>5} | {'Penjualan':>11} | {'Total Profit':>12} | {'Margin':>7}"
    )
    print(ROW_DIVIDER)

    for idx, item in enumerate(results, start=1):
        short_name = format_truncate(item["product_name"], 26)
        short_brand = format_truncate(item["brand"], 15)
        print(
            f"{idx:<4} | {item['product_id']:<11} | {short_brand:<15} | {short_name:<26} | "
            f"{item['total_quantity']:>5} | ${item['total_net_sales']:>10,.2f} | "
            f"${item['total_profit']:>11,.2f} | {item['profit_margin']:>6.1f}%"
        )
    print(TABLE_DIVIDER)


def display_category_contribution(catalog: EcommerceCatalog) -> None:
    """Menampilkan Target 2: Kategori yang paling berkontribusi terhadap total penjualan."""
    print("\n--- [FITUR 2] KONTRIBUSI KATEGORI TERHADAP TOTAL PENJUALAN ---")
    top_n = prompt_int("Masukkan jumlah kategori teratas yang ingin ditampilkan (1-117): ", 1, 117)
    results = get_category_sales_contribution(catalog, top_n=top_n)

    if not results:
        print("  Tidak ada data kategori untuk ditampilkan.")
        return

    print("\n" + TABLE_DIVIDER)
    print(
        f"{'No':<4} | {'Subkategori Produk':<24} | {'Order':>6} | {'Qty':>6} | "
        f"{'Total Penjualan':>15} | {'Total Profit':>13} | {'Rata2/Order':>11} | {'Kontribusi':>10}"
    )
    print(ROW_DIVIDER)

    for idx, item in enumerate(results, start=1):
        short_cat = format_truncate(item["subcategory"], 24)
        print(
            f"{idx:<4} | {short_cat:<24} | {item['order_count']:>6} | {item['total_quantity']:>6} | "
            f"${item['total_net_sales']:>14,.2f} | ${item['total_profit']:>12,.2f} | "
            f"${item['avg_order_sales']:>10,.2f} | {item['sales_contribution_pct']:>9.2f}%"
        )
    print(TABLE_DIVIDER)


def display_top_brands(catalog: EcommerceCatalog) -> None:
    """Menampilkan Target 3: Merek (Brand) dengan kinerja terbaik."""
    print("\n--- [FITUR 3] MEREK (BRAND) BERKINERJA TERBAIK ---")
    print("Pilih dasar pengurutan kinerja merek:")
    print("  1. Berdasarkan Total Profit Tertinggi")
    print("  2. Berdasarkan Total Penjualan Bersih (Net Sales) Tertinggi")
    print("  3. Berdasarkan Persentase Margin Profit Tertinggi")

    sort_choice = prompt_int("Pilihan pengurutan (1-3): ", 1, 3)
    if sort_choice == 1:
        sort_key = "total_profit"
    elif sort_choice == 2:
        sort_key = "total_net_sales"
    else:
        sort_key = "profit_margin"

    top_n = prompt_int("Masukkan jumlah merek teratas yang ingin ditampilkan (1-50): ", 1, 50)
    results = get_top_performing_brands(catalog, sort_by=sort_key, top_n=top_n)

    if not results:
        print("  Tidak ada data merek untuk ditampilkan.")
        return

    print("\n" + TABLE_DIVIDER)
    print(
        f"{'No':<4} | {'Nama Merek':<18} | {'Order':>5} | {'Qty':>5} | "
        f"{'Total Penjualan':>14} | {'Total Profit':>12} | {'Margin':>7} | {'Status Kinerja':<16}"
    )
    print(ROW_DIVIDER)

    for idx, item in enumerate(results, start=1):
        short_brand = format_truncate(item["brand"], 18)
        print(
            f"{idx:<4} | {short_brand:<18} | {item['order_count']:>5} | {item['total_quantity']:>5} | "
            f"${item['total_net_sales']:>13,.2f} | ${item['total_profit']:>11,.2f} | "
            f"{item['profit_margin']:>6.1f}% | {item['brand_status']:<16}"
        )
    print(TABLE_DIVIDER)


def print_record_list(records: list[OrderRecord], max_display: int = 20) -> None:
    """Mencetak daftar objek OrderRecord dalam tabel sejajar menggunakan __str__."""
    if not records:
        print("  [i] Tidak ditemukan data transaksi yang sesuai kriteria.")
        return

    total_found = len(records)
    displayed = records[:max_display]

    print(f"\nMenampilkan {len(displayed)} dari {total_found} transaksi yang cocok:")
    print(TABLE_DIVIDER)
    print(
        f"{'ID Produk':<12} | {'Merek':<16} | {'Nama Produk':<30} | "
        f"{'Subkategori':<18} | {'Qty':>4} | {'Penjualan':>11} | {'Profit':>10} | {'Margin':>7}"
    )
    print(ROW_DIVIDER)

    for rec in displayed:
        print(rec)

    print(TABLE_DIVIDER)


def handle_search(catalog: EcommerceCatalog) -> None:
    """Menangani Fitur 4: Pencarian kata kunci bebas."""
    print("\n--- [FITUR 4] PENCARIAN TRANSAKSI & PRODUK ---")
    while True:
        keyword = input("Masukkan kata kunci (Nama Produk / Merek / Kategori / ID): ").strip()
        if keyword != "":
            break
        print("  [!] Kata kunci tidak boleh kosong. Silakan ketik sesuatu.")

    matches = search_records(catalog, keyword)
    print_record_list(matches, max_display=20)


def handle_filter(catalog: EcommerceCatalog) -> None:
    """Menangani Fitur 5: Penyaringan transaksi multi-kriteria."""
    print("\n--- [FITUR 5] FILTER TRANSAKSI MULTI-KRITERIA ---")
    only_profit = prompt_yes_no("Hanya tampilkan transaksi yang untung/profit positif? (y/n): ")
    min_profit = prompt_float("Masukkan nilai profit minimum dalam $ (contoh: 50 atau 0): ", -50000.0)
    subcat = input("Masukkan filter nama subkategori (tekan Enter untuk semua kategori): ").strip()

    filtered = filter_records_by_criteria(
        catalog=catalog,
        min_profit=min_profit,
        only_profitable=only_profit,
        subcategory_query=subcat,
    )
    print_record_list(filtered, max_display=20)


# ==========================================
# FUNGSI UTAMA & MENU LOOP (while)
# ==========================================
def print_menu() -> None:
    """Menampilkan daftar menu utama aplikasi."""
    print("\n" + "=" * 62)
    print("   SISTEM ANALISIS PENJUALAN & PROFITABILITAS E-COMMERCE")
    print("=" * 62)
    print("  1. Produk dengan Keuntungan Tertinggi (Top-N Produk)")
    print("  2. Kontribusi Kategori terhadap Total Penjualan")
    print("  3. Merek (Brand) Berkinerja Terbaik")
    print("  4. Cari Produk / Merek / Subkategori (Pencarian Teks)")
    print("  5. Filter Transaksi Berdasarkan Profit & Kategori")
    print("  6. Ringkasan Statistik Dataset Keseluruhan")
    print("  0. Keluar dari Program")
    print("=" * 62)


def main() -> None:
    """Fungsi utama untuk memuat data dan menjalankan loop menu interaktif."""
    print("Memuat dataset dari file:", CSV_FILENAME)
    try:
        catalog = load_dataset(CSV_FILENAME)
    except FileNotFoundError as err:
        print(f"[ERROR] {err}")
        print("Pastikan file CSV berada di folder yang sama dengan main.py.")
        return

    # Melaporkan jumlah baris yang berhasil dimuat dan jumlah baris rusak yang dilewati
    print(f"Berhasil memuat : {catalog.total_records()} baris transaksi valid.")
    print(f"Baris dilewati  : {catalog.skipped_rows} baris (format angka/data rusak).")

    # Perulangan while untuk menu utama hingga pengguna memilih Keluar ('0')
    is_running = True
    while is_running:
        print_menu()
        choice = input("Pilih menu (0-6): ").strip()

        if choice == "1":
            display_top_products(catalog)
        elif choice == "2":
            display_category_contribution(catalog)
        elif choice == "3":
            display_top_brands(catalog)
        elif choice == "4":
            handle_search(catalog)
        elif choice == "5":
            handle_filter(catalog)
        elif choice == "6":
            print("\n--- [FITUR 6] RINGKASAN DATASET E-COMMERCE ---")
            print(catalog)
            print(f"Total Keuntungan Bersih (Profit): ${catalog.get_total_profit():,.2f}")
        elif choice == "0":
            print("\nTerima kasih telah menggunakan program analisis E-Commerce. Sampai jumpa!")
            is_running = False
        else:
            print(
                f"\n  [!] Pilihan '{choice}' tidak valid. Silakan ketik angka antara 0 sampai 6."
            )


if __name__ == "__main__":
    main()