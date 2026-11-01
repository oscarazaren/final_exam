"""
text_utils.py
Berisi fungsi-fungsi pembantu untuk manipulasi dan pembersihan string.
"""


def clean_text(text: str) -> str:
    """
    Membersihkan teks untuk perbandingan/pencarian yang mengabaikan huruf kapital
    dan spasi tambahan: mengubah ke huruf kecil (lower), menghapus tanda hubung/kutip
    (replace), serta merapikan spasi berlebih (strip & split).
    """
    if not isinstance(text, str):
        return ""
    cleaned = text.lower().strip()
    cleaned = cleaned.replace("-", " ").replace("'", "").replace("&", "and")
    words = cleaned.split()
    return " ".join(words)


def extract_brand(product_name: str, subcategory: str = "") -> str:
    """
    Mengekstrak nama merek (brand) dari nama produk pada dataset e-commerce.
    Format product_name di CSV: [Nama Brand] [Kata Slogan Kapital] [kata slogan kecil...] [Subcategory]
    """
    if not isinstance(product_name, str) or not product_name.strip():
        return "Unknown"

    text = product_name.strip()
    # Hapus nama subkategori di bagian akhir jika cocok
    if subcategory and text.endswith(subcategory):
        text = text[: -len(subcategory)].strip()

    words = text.split()
    if len(words) <= 1:
        return text

    # Cari indeks di mana kata deskripsi/slogan dimulai (diawali huruf kecil atau angka selain '21')
    brand_end_idx = 1
    for i in range(1, len(words)):
        word = words[i]
        if word[0].islower() or (word[0].isdigit() and word != "21"):
            brand_end_idx = i - 1
            break

    if brand_end_idx < 1:
        brand_end_idx = 1

    return " ".join(words[:brand_end_idx])


def format_truncate(text: str, max_length: int = 30) -> str:
    """
    Memotong teks yang terlalu panjang dan menambahkan '..' agar tampilan
    kolom tabel tetap sejajar dan rapi.
    """
    if not isinstance(text, str):
        return ""
    clean = text.strip()
    if max_length < 4:
        return clean[:max_length]
    if len(clean) > max_length:
        return clean[: max_length - 2] + ".."
    return clean