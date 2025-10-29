from tracker.rekap_kelas import RekapKelas
from tracker.mahasiswa import Mahasiswa
from tracker.report import build_markdown_report, save_text
import csv

def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def bootstrap_from_csv(rekap, att_path, grd_path):
    att = load_csv(att_path)
    grd = load_csv(grd_path)
    # index nilai by NIM
    by_nim = {g["student_id"]: g for g in grd}

    for row in att:
        nim = row["student_id"].strip()
        nama = row["name"].strip()
        m = Mahasiswa(nim, nama)
        # tambah mahasiswa (unik)
        try:
            rekap.tambah_mahasiswa(m)
        except KeyError:
            pass
        # hitung hadir %
        weeks = [k for k in row.keys() if k.startswith("week")]
        if weeks:
            total = len(weeks)
            hadir = 0
            for w in weeks:
                val = row[w].strip()
                if val != "":
                    hadir += int(val)
            persen = round(hadir/total*100.0, 2)
            rekap.set_hadir(nim, persen)
        # isi nilai jika ada
        g = by_nim.get(nim)
        if g:
            def _num(x):
                try: return float(x)
                except: return 0.0
            rekap.set_penilaian(
                nim,
                quiz=_num(g.get("quiz", 0)),
                tugas=_num(g.get("assignment", 0)),
                uts=_num(g.get("mid", 0)),
                uas=_num(g.get("final", 0)),
            )

def tampilkan_rekap(rows):
    print("\nNIM        | Nama       | Hadir% | Akhir | Pred")
    print("-----------------------------------------------")
    for r in rows:
        print("{:<10} | {:<10} | {:>6.2f} | {:>5.2f} | {}".format(
            r['nim'], r['nama'], r['hadir'], r['akhir'], r['predikat']
        ))
    print()

def menu():
    r = RekapKelas()
    while True:
        print("=== Student Performance Tracker ===")
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
                bootstrap_from_csv(r, "data/attendance.csv", "data/grades.csv")
                print("OK, data dimuat.")
            elif pilih == "2":
                nim = input("NIM: ").strip()
                nama = input("Nama: ").strip()
                r.tambah_mahasiswa(Mahasiswa(nim, nama))
                print("Mahasiswa ditambah.")
            elif pilih == "3":
                nim = input("NIM: ").strip()
                hadir = float(input("Hadir %: ").strip())
                r.set_hadir(nim, hadir)
                print("Hadir diset.")
            elif pilih == "4":
                nim = input("NIM: ").strip()
                q = float(input("Quiz: ").strip())
                t = float(input("Tugas: ").strip())
                u = float(input("UTS: ").strip())
                a = float(input("UAS: ").strip())
                r.set_penilaian(nim, quiz=q, tugas=t, uts=u, uas=a)
                print("Nilai diset.")
            elif pilih == "5":
                tampilkan_rekap(r.rekap())
            elif pilih == "6":
                md = build_markdown_report(r.rekap())
                save_text("out/report.md", md)
                print("✅ Laporan tersimpan di out/report.md")
            elif pilih == "7":
                rows = r.filter_bawah_70()
                if not rows:
                    print("Semua mahasiswa nilainya >= 70.")
                else:
                    tampilkan_rekap(rows)
            elif pilih == "8":
                from tracker.report import build_html_report, save_html
                html = build_html_report(r.rekap())
                save_html("out/report.html", html)
                print("✅ Laporan HTML tersimpan di out/report.html")
            elif pilih == "9":
                print("Dadah."); break
            else:
                print("Pilihan tidak dikenal.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    menu()
