import os
import csv
from tracker.rekap_kelas import RekapKelas
from tracker.mahasiswa import Mahasiswa
from tracker.report import build_markdown_report, save_text

# ===== util tampilan =====
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(msg="Tekan Enter untuk lanjut..."):
    try:
        input(msg)
    except EOFError:
        pass

def header(title="Student Performance Tracker"):
    print(f"=== {title} ===")

# ===== io csv =====
def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def bootstrap_from_csv(rekap, att_path, grd_path):
    att = load_csv(att_path)
    grd = load_csv(grd_path)
    by_nim = {g["student_id"]: g for g in grd}

    for row in att:
        nim = row["student_id"].strip()
        nama = row["name"].strip()
        m = Mahasiswa(nim, nama)
        try:
            rekap.tambah_mahasiswa(m)
        except KeyError:
            pass

        weeks = [k for k in row.keys() if k.startswith("week")]
        if weeks:
            total = len(weeks)
            hadir = 0
            for w in weeks:
                val = row[w].strip()
                if val != "":
                    hadir += int(val)
            persen = round(hadir / total * 100.0, 2)
            rekap.set_hadir(nim, persen)

        g = by_nim.get(nim)
        if g:
            def _num(x):
                try:
                    return float(x)
                except:
                    return 0.0
            rekap.set_penilaian(
                nim,
                quiz=_num(g.get("quiz", 0)),
                tugas=_num(g.get("assignment", 0)),
                uts=_num(g.get("mid", 0)),
                uas=_num(g.get("final", 0)),
            )

# ===== view tabel =====
def tampilkan_rekap(rows):
    print("\nNIM        | Nama       | Hadir% | Akhir | Pred")
    print("-----------------------------------------------")
    for r in rows:
        print("{:<10} | {:<10} | {:>6.2f} | {:>5.2f} | {}".format(
            r['nim'], r['nama'], r['hadir'], r['akhir'], r['predikat']
        ))
    print()

# ===== menu utama dengan auto-clear =====
def menu():
    r = RekapKelas()
    while True:
        clear_screen()
        header("Student Performance Tracker")
        print("1) Muat data dari CSV")
        print("2) Tambah mahasiswa")
        print("3) Ubah presensi")
        print("4) Ubah nilai")
        print("5) Lihat rekap")
        print("6) Simpan laporan Markdown")
        print("7) Filter nilai < 70 (remedial)")
        print("8) Simpan laporan HTML berwarna")
        print("9) Keluar")
        pilih = input("Pilih: ").strip()

        try:
            if pilih == "1":
                clear_screen()
                header("Muat data dari CSV")
                bootstrap_from_csv(r, "data/attendance.csv", "data/grades.csv")
                print("✅ OK, data dimuat.")
                pause()

            elif pilih == "2":
                clear_screen()
                header("Tambah mahasiswa")
                nim = input("NIM: ").strip()
                nama = input("Nama: ").strip()
                r.tambah_mahasiswa(Mahasiswa(nim, nama))
                print("✅ Mahasiswa ditambah.")
                pause()

            elif pilih == "3":
                clear_screen()
                header("Ubah presensi")
                nim = input("NIM: ").strip()
                hadir = float(input("Hadir %: ").strip())
                r.set_hadir(nim, hadir)
                print("✅ Hadir diset.")
                pause()

            elif pilih == "4":
                clear_screen()
                header("Ubah nilai")
                nim = input("NIM: ").strip()
                q = float(input("Quiz: ").strip())
                t = float(input("Tugas: ").strip())
                u = float(input("UTS: ").strip())
                a = float(input("UAS: ").strip())
                r.set_penilaian(nim, quiz=q, tugas=t, uts=u, uas=a)
                print("✅ Nilai diset.")
                pause()

            elif pilih == "5":
                clear_screen()
                header("Rekap nilai")
                tampilkan_rekap(r.rekap())
                pause()

            elif pilih == "6":
                clear_screen()
                header("Simpan laporan Markdown")
                md = build_markdown_report(r.rekap())
                save_text("out/report.md", md)
                print("✅ Laporan tersimpan di out/report.md")
                pause()

            elif pilih == "7":
                clear_screen()
                header("Filter nilai < 70 (remedial)")
                rows = r.filter_bawah_70()
                if not rows:
                    print("Semua mahasiswa nilainya >= 70.")
                else:
                    tampilkan_rekap(rows)
                pause()

            elif pilih == "8":
                clear_screen()
                header("Simpan laporan HTML")
                from tracker.report import build_html_report, save_html
                html = build_html_report(r.rekap())
                save_html("out/report.html", html)
                print("✅ Laporan HTML tersimpan di out/report.html")
                pause()

            elif pilih == "9":
                clear_screen()
                print("Dadah 👋")
                break

            else:
                clear_screen()
                print("❌ Pilihan tidak dikenal.")
                pause()

        except Exception as e:
            clear_screen()
            print("💥 Error:", e)
            pause()

if __name__ == "__main__":
    menu()
