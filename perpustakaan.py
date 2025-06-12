import json
from datetime import datetime
from collections import deque

# Algoritma Sorting: Quick Sort
def quick_sort(arr, key):
    # Jika panjang array kurang dari atau sama dengan 1, sudah terurut
    if len(arr) <= 1:
        return arr
    # Menentukan pivot, yaitu elemen tengah
    pivot = arr[len(arr) // 2]
    # Membagi array berdasarkan nilai key yang lebih kecil, sama dengan, dan lebih besar dari pivot
    left = [x for x in arr if getattr(x, key) < getattr(pivot, key)]
    middle = [x for x in arr if getattr(x, key) == getattr(pivot, key)]
    right = [x for x in arr if getattr(x, key) > getattr(pivot, key)]
    # Rekursif untuk mengurutkan bagian kiri dan kanan
    return quick_sort(left, key) + middle + quick_sort(right, key)

# Algoritma Searching: Binary Search
def binary_search(arr, key, target):
    # Menetapkan batas kiri dan kanan
    left, right = 0, len(arr) - 1
    # Melakukan pencarian hingga batas kiri melebihi batas kanan
    while left <= right:
        mid = (left + right) // 2
        # Jika elemen di tengah adalah target, kembalikan indeksnya
        if getattr(arr[mid], key) == target:
            return mid
        # Jika elemen di tengah lebih kecil dari target, cari di bagian kanan
        elif getattr(arr[mid], key) < target:
            left = mid + 1
        # Jika elemen di tengah lebih besar dari target, cari di bagian kiri
        else:
            right = mid - 1
    # Jika tidak ditemukan, kembalikan -1
    return -1

# Class Buku
class Buku:
    def __init__(self, judul, pengarang, tahun):
        # Konstruktor untuk inisialisasi atribut buku
        self.judul = judul
        self.pengarang = pengarang
        self.tahun = tahun
        self.dipinjam = False
        self.tanggal_peminjaman = None
        self.antrian_peminjam = deque()

    def to_dict(self):
        # Mengkonversi objek Buku ke bentuk dictionary
        return {
            "judul": self.judul,
            "pengarang": self.pengarang,
            "tahun": self.tahun,
            "dipinjam": self.dipinjam,
            "tanggal_peminjaman": self.tanggal_peminjaman,
            "antrian_peminjam": list(self.antrian_peminjam)
        }

    @staticmethod
    def from_dict(data):
        # Mengkonversi dictionary ke objek Buku
        buku = Buku(data["judul"], data["pengarang"], data["tahun"])
        buku.dipinjam = data["dipinjam"]
        buku.tanggal_peminjaman = data.get("tanggal_peminjaman")
        buku.antrian_peminjam = deque(data.get("antrian_peminjam", []))
        return buku

    def __str__(self):
        # Menampilkan informasi buku dalam format string
        status = 'Dipinjam' if self.dipinjam else 'Tersedia'
        return f"{self.judul} - {self.pengarang} ({self.tahun}) [{status}]"

# Class Perpustakaan
class Perpustakaan:
    def __init__(self, filename="perpustakaan.json"):
        # Konstruktor untuk inisialisasi perpustakaan dan memuat data
        self.filename = filename
        self.koleksi_buku = []
        self.load_data()
        if not self.koleksi_buku:
            self.init_default_books()

    def simpan_data(self):
        # Menyimpan data koleksi buku ke dalam file JSON
        with open(self.filename, "w") as file:
            json.dump([buku.to_dict() for buku in self.koleksi_buku], file, indent=4)

    def load_data(self):
        # Memuat data koleksi buku dari file JSON
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.koleksi_buku = [Buku.from_dict(b) for b in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.koleksi_buku = []

    def init_default_books(self):
        # Menambahkan buku default jika koleksi kosong
        default_books = [
            ("Pemrograman Python", "Guido van Rossum", 2010),
            ("Algoritma dan Struktur Data", "Donald Knuth", 2005),
            ("Machine Learning", "Andrew Ng", 2018),
            ("Clean Code", "Robert C. Martin", 2008),
            ("The Pragmatic Programmer", "Andrew Hunt dan David Thomas", 1999),
            ("Introduction to Algorithms", "Thomas H. Cormen", 2009),
            ("Design Patterns", "Erich Gamma et al.", 1994),
            ("Automate the Boring Stuff with Python", "Al Sweigart", 2015),
            ("Eloquent JavaScript", "Marijn Haverbeke", 2011)
        ]

        for judul, pengarang, tahun in default_books:
            self.koleksi_buku.append(Buku(judul, pengarang, tahun))
        self.simpan_data()

    def tampilkan_buku(self):
        # Menampilkan daftar buku yang terurut berdasarkan judul
        if not self.koleksi_buku:
            print("Tidak ada buku dalam perpustakaan!\n")
            return
        self.koleksi_buku = quick_sort(self.koleksi_buku, "judul")
        print("\nDaftar Buku:")
        for i, buku in enumerate(self.koleksi_buku, start=1):
            print(f"{i}. {buku}")
        print()

    def tambah_buku(self, judul, pengarang, tahun):
        # Menambahkan buku baru ke koleksi
        self.koleksi_buku.append(Buku(judul, pengarang, tahun))
        self.simpan_data()
        print(f"Buku '{judul}' berhasil ditambahkan!")

    def hapus_buku(self, index):
        # Menghapus buku berdasarkan indeks
        if 0 <= index < len(self.koleksi_buku):
            buku = self.koleksi_buku.pop(index)
            self.simpan_data()
            print(f"Buku '{buku.judul}' berhasil dihapus!")
        else:
            print("Nomor buku tidak valid!")

    def cari_buku(self, judul):
        # Mencari buku berdasarkan judul menggunakan binary search
        self.koleksi_buku = quick_sort(self.koleksi_buku, "judul")
        index = binary_search(self.koleksi_buku, "judul", judul)
        if index != -1:
            print(f"Buku ditemukan: {self.koleksi_buku[index]}")
        else:
            print("Buku tidak ditemukan!")

    def lihat_antrian(self):
        # Menampilkan antrian peminjam untuk buku yang sedang dipinjam
        for buku in self.koleksi_buku:
            if buku.antrian_peminjam:
                print(f"{buku.judul}: {list(buku.antrian_peminjam)}")

    def pinjam_buku(self, index, nama_peminjam):
        # Meminjam buku atau menambah peminjam ke antrian jika buku sudah dipinjam
        if 0 <= index < len(self.koleksi_buku):
            buku = self.koleksi_buku[index]
            if not buku.dipinjam:
                buku.dipinjam = True
                buku.tanggal_peminjaman = datetime.now().strftime("%Y-%m-%d")
                print(f"Buku '{buku.judul}' berhasil dipinjam oleh {nama_peminjam}!")
            else:
                buku.antrian_peminjam.append(nama_peminjam)
                print(f"Buku sedang dipinjam. {nama_peminjam} masuk dalam antrian.")
            self.simpan_data()
        else:
            print("Nomor buku tidak valid!")

    def kembalikan_buku(self, index):
        # Mengembalikan buku dan memproses peminjam berikutnya dari antrian jika ada
        if 0 <= index < len(self.koleksi_buku):
            buku = self.koleksi_buku[index]
            if buku.dipinjam:
                buku.dipinjam = False
                buku.tanggal_peminjaman = None
                if buku.antrian_peminjam:
                    peminjam_selanjutnya = buku.antrian_peminjam.popleft()
                    buku.dipinjam = True
                    buku.tanggal_peminjaman = datetime.now().strftime("%Y-%m-%d")
                    print(f"Buku '{buku.judul}' sekarang dipinjam oleh {peminjam_selanjutnya}!")
                else:
                    print(f"Buku '{buku.judul}' berhasil dikembalikan!")
                self.simpan_data()
            else:
                print("Buku ini tidak sedang dipinjam!")
        else:
            print("Nomor buku tidak valid!")

# Username Admin dan Password
username_password = {
    "Ahmad": "123",
    "Ruden": "456",
    "Zaidan": "789"
}

def admin_login(maksimal_percobaan=3):
    # Fungsi untuk login sebagai admin dengan batas percobaan
    percobaan = 0
    while percobaan < maksimal_percobaan:
        username = input("\nMasukkan username: ")
        password = input("Masukkan password: ")
        if username in username_password and username_password[username] == password:
            return True
        else:
            percobaan += 1
            print(f"\nUsername atau password salah! Coba lagi. ({maksimal_percobaan - percobaan} percobaan tersisa)")
    return False

# Menu Admin
def admin():
    # Memeriksa login admin
    if not admin_login():
        print("Terlalu banyak percobaan. Akses ditolak.")
        return

    perpus = Perpustakaan()
    while True:
        # Menampilkan menu admin
        print("\nMenu Perpustakaan:")
        print("1. Tampilkan Buku")
        print("2. Tambah Buku")
        print("3. Hapus Buku")
        print("4. Cari Buku")
        print("5. Lihat Antrian Peminjam")
        print("6. Keluar")

        pilihan = input("Masukkan pilihan: ")

        # Menangani pilihan menu admin
        if pilihan == "1":
            perpus.tampilkan_buku()
        elif pilihan == "2":
            judul = input("Masukkan judul buku: ")
            pengarang = input("Masukkan pengarang: ")
            tahun = int(input("Masukkan tahun terbit: "))
            perpus.tambah_buku(judul, pengarang, tahun)
        elif pilihan == "3":
            perpus.tampilkan_buku()
            index = int(input("Masukkan nomor buku yang ingin dihapus: ")) - 1
            perpus.hapus_buku(index)
        elif pilihan == "4":
            judul = input("Masukkan judul buku yang dicari: ")
            perpus.cari_buku(judul)
        elif pilihan == "5":
            perpus.lihat_antrian()
        elif pilihan == "6":
            print("Terima kasih telah menggunakan sistem perpustakaan!")
            break
        else:
            print("Pilihan tidak valid!")

# Menu User
def user():
    perpus = Perpustakaan()
    while True:
        # Menampilkan menu user
        print("\nMenu Perpustakaan:")
        print("1. Tampilkan Buku")
        print("2. Cari Buku")
        print("3. Pinjam Buku")
        print("4. Kembalikan Buku")
        print("5. Keluar")

        pilihan = input("Masukkan pilihan: ")

        # Menangani pilihan menu user
        if pilihan == "1":
            perpus.tampilkan_buku()
        elif pilihan == "2":
            judul = input("Masukkan judul buku yang dicari: ")
            perpus.cari_buku(judul)
        elif pilihan == "3":
            perpus.tampilkan_buku()
            index = int(input("Masukkan nomor buku yang ingin dipinjam: ")) - 1
            nama_peminjam = input("Masukkan nama peminjam: ")
            perpus.pinjam_buku(index, nama_peminjam)
        elif pilihan == "4":
            perpus.tampilkan_buku()
            index = int(input("Masukkan nomor buku yang ingin dikembalikan: ")) - 1
            perpus.kembalikan_buku(index)
        elif pilihan == "5":
            print("Terima kasih telah menggunakan sistem perpustakaan!")
            break
        else:
            print("Pilihan tidak valid!")

# Memilih untuk login sebagai admin atau user
def main():
    print("Selamat datang di Perpustakaan Digital!")

    while True:
        print("\nPilih mode:")
        print("1. Admin")
        print("2. User")
        print("3. Keluar")

        mode = input("Masukkan pilihan: ")

        if mode == "1":
            admin()
        elif mode == "2":
            user()
        elif mode == "3":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
