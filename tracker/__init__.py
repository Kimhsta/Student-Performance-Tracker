# tracker/__init__.py
def main():
    """Entry point saat menjalankan: python3 -m tracker"""
    from .rekap_kelas import RekapKelas
    from .mahasiswa import Mahasiswa
    from .report import build_markdown_report, save_text

    r = RekapKelas()
    # contoh data mini biar kelihatan jalan
    m = Mahasiswa("230101999", "Tester")
    r.tambah_mahasiswa(m)
    r.set_hadir("230101999", 90)
    r.set_penilaian("230101999", quiz=80, tugas=85, uts=80, uas=90)

    md = build_markdown_report(r.rekap())
    save_text("out/report_mod.md", md)
    print("✅ tracker berhasil dijalankan (lihat out/report_mod.md)")
