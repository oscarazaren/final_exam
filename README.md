# Analisis Penjualan & Profitabilitas E-Commerce (Proyek Ujian Akhir Pemrograman Komputer)

Program berbasis menu (*Command-Line Interface*) yang dibangun dengan **Pure Python 3** (hanya menggunakan pustaka standar Python tanpa modul eksternal seperti Pandas atau NumPy) untuk mengeksplorasi dan menganalisis dataset transaksi e-commerce nyata.

---

## 📁 Informasi Dataset
* **Dataset Name:** Data Analisis Penjualan Produk Marketplace
* **Kaggle Link:** [E-Commerce Sales and Customer Analytics on Kaggle](https://www.kaggle.com/datasets/datascikhan/e-commerce-sales-and-customer-analytics/data)
* **Keterangan Modifikasi CSV:**
  * Data dipotong menjadi **1.498 baris** transaksi.
  * Penambahan kolom `product_name` pada kolom C dan `product_subcategory` pada kolom D.
  * *Note:* Penambahan kategori didasarkan pada data `product_catalog` yang tersedia di dataset dan digabungkan menggunakan rumus spreadsheet untuk menyederhanakan struktur program.

---

## 💡 Alasan Memilih Dataset (*Why You Choose It*)
Dataset ini dipilih karena tren e-commerce di Indonesia saat ini sedang berkembang pesat, dan para *seller* memerlukan analisis produk yang tepat secara data-driven dalam pengambilan keputusan bisnis mereka, terutama untuk mengetahui produk, kategori, dan merek yang paling menguntungkan.

---

## 🎯 Target & Fitur Aplikasi
Aplikasi ini dirancang untuk menjawab 3 pertanyaan bisnis utama melalui 6 fitur interaktif:
1. **Produk Mana yang Menghasilkan Keuntungan Tertinggi?** (Fitur 1: Top-N Produk berdasarkan *profit* dan margin).
2. **Kategori Mana yang Paling Berkontribusi Terhadap Total Penjualan?** (Fitur 2: Kontribusi persentase penjualan bersih per subkategori).
3. **Merek Mana yang Berkinerja Terbaik?** (Fitur 3: Evaluasi *brand* berdasarkan profit, omzet, dan predikat kinerja).
4. **Pencarian Bebas (Fitur 4):** Mencari produk, merek, atau subkategori secara fleksibel (kebal terhadap perbedaan huruf besar/kecil dan spasi berlebih).
5. **Filter Multi-Kriteria (Fitur 5):** Menyaring transaksi berdasarkan batas minimum profit dan subkategori menggunakan operator logika.
6. **Ringkasan Statistik Keseluruhan (Fitur 6):** Menampilkan total keseluruhan penjualan bersih, total profit, dan metadata pemuatan data.

---

## 🛠️ Struktur File Proyek (.py)
Sistem ini dibangun secara modular ke dalam 6 file Python:
1. **`text_utils.py`** — Berisi fungsi pembantu manipulasi string (`clean_text`, `extract_brand`, `format_truncate`).
2. **`models.py`** — Menyimpan konstanta global, Class `OrderRecord` (menyimpan 1 baris record, nilai turunan, dan perhitungan margin), serta Class `EcommerceCatalog` (koleksi list record).
3. **`data_loader.py`** — Membaca file CSV dengan modul `csv`, memvalidasi kelengkapan data, serta melewati dan melaporkan baris data yang rusak (*skipped rows*).
4. **`analysis.py`** — Berisi algoritma analisis dan **pengurutan manual (Selection Sort dengan perulangan `for` bersarang tanpa fungsi `sorted()` bawaan)** serta pemotongan list (*slicing*).
5. **`main.py`** — Titik masuk utama program (`python main.py`), menangani menu interaktif (`while` loop), validasi input anti-*crash*, dan pencetakan tabel dengan kolom sejajar (*f-string*).
6. **`test_project.py`** — Modul pengujian unit menggunakan pustaka standar `unittest` untuk menguji input normal, *edge cases*, dan input buruk.

---

## ⚠️ Keterbatasan yang Diketahui (*Known Limitations*)
* Pada file CSV asli, terdapat **194 baris** data yang memiliki anomali format angka pada kolom tertentu (seperti `shipping_cost`). Program menangani keterbatasan ini secara otomatis dengan melewati baris yang rusak, memuat **1.304 baris data valid**, dan melaporkan jumlah baris yang dilewati saat program dimulai.

| Konsep Python | File tempat digunakan | Fungsi / Bagian Kode tempat diterapkan |
| :--- | :--- | :--- |
| **Variabel & Tipe Data** | `models.py`, `main.py` | Menyimpan tipe data `str`, `int`, `float`, `bool`, `list`, dan konstanta huruf kapital (`CSV_FILENAME`, `HIGH_MARGIN_THRESHOLD`). |
| **Masukan & Keluaran** | `main.py` | Membaca input dengan `input()`, validasi dalam *loop* `while True`, dan pencetakan tabel sejajar dengan *f-string*. |
| **Operator** | `models.py`, `analysis.py` | Operator aritmatika (menghitung `profit_margin` & `discount_rate`), relasional (`>`, `>=`, `<=`), dan logika (`and`, `or`, `not`). |
| **Pernyataan Bersyarat** | `models.py`, `analysis.py` | Penggunaan `if-elif-else` untuk mengelompokkan kategori performa produk dan status kinerja merek. |
| **Pernyataan Perulangan** | `analysis.py`, `main.py` | Perulangan `for` untuk pemrosesan data/pengurutan manual (*Selection Sort*) dan `while` untuk menu utama. |
| **Fungsi** | Seluruh file `.py` | Fungsi modular yang menerima parameter dan mengembalikan nilai kembalian (*return value*). |
| **Daftar (List) & Slicing** | `models.py`, `analysis.py` | Menyimpan koleksi objek dalam `list`, membuat daftar turunan hasil filter, dan teknik *slicing* (`[:top_n]`). |
| **Manipulasi String** | `text_utils.py` | Fungsi pembersih teks menggunakan metode `.lower()`, `.strip()`, `.replace()`, dan `.split()`. |
| **Kelas (OOP - Bonus)** | `models.py` | Class `OrderRecord` (memiliki `__init__` dan `__str__`) serta Class `EcommerceCatalog` untuk menyimpan koleksi data. |
| **Pengujian Unit** | `test_project.py` | Modul `unittest` dengan 5+ pengujian mencakup input normal, *edge cases*, dan input buruk. |

---
 
