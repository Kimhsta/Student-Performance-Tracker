"""Manajer rekap: menyatukan Mahasiswa + Penilaian + util predikat."""

from .mahasiswa import Mahasiswa
from .penilaian import Penilaian


class RekapKelas:
    """Menyimpan daftar mahasiswa dan penilaian, serta menghasilkan rekap."""

    def __init__(self):
        # nim -> {'mhs': Mahasiswa, 'nilai': Penilaian}
        self._by_nim = {}

    def tambah_mahasiswa(self, mhs):
        """Tambahkan objek Mahasiswa (NIM unik)."""
        if mhs.nim in self._by_nim:
            raise KeyError("NIM sudah terdaftar")
        self._by_nim[mhs.nim] = {'mhs': mhs, 'nilai': Penilaian()}

    def set_hadir(self, nim, persen):
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError("NIM tidak ditemukan")
        item['mhs'].hadir_persen = persen

    def set_penilaian(self, nim, quiz=None, tugas=None, uts=None, uas=None):
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError("NIM tidak ditemukan")
        p = item['nilai']
        if quiz is not None:
            p.quiz = quiz
        if tugas is not None:
            p.tugas = tugas
        if uts is not None:
            p.uts = uts
        if uas is not None:
            p.uas = uas

    def predikat(self, skor):
        if skor >= 85:
            return "A"
        if skor >= 75:
            return "B"
        if skor >= 65:
            return "C"
        if skor >= 50:
            return "D"
        return "E"

    def rekap(self):
        """Kembalikan list of dict: nim, nama, hadir, akhir, predikat."""
        rows = []
        for nim, d in self._by_nim.items():
            m = d['mhs']
            p = d['nilai']
            akhir = p.nilai_akhir()
            rows.append({
                'nim': nim,
                'nama': m.nama,
                'hadir': m.hadir_persen,
                'akhir': akhir,
                'predikat': self.predikat(akhir),
            })
        return rows

    def filter_bawah_70(self):
        """Kembalikan hanya mahasiswa dengan nilai akhir < 70."""
        hasil = []
        for nim, d in self._by_nim.items():
            p = d['nilai']
            skor = p.nilai_akhir()
            if skor < 70:
                m = d['mhs']
                hasil.append({
                    'nim': m.nim,
                    'nama': m.nama,
                    'hadir': m.hadir_persen,
                    'akhir': skor,
                    'predikat': self.predikat(skor),
                })
        return hasil

    # util opsional untuk load cepat dari dict simple
    def tambah_mahasiswa_manual(self, nim, nama):
        self.tambah_mahasiswa(Mahasiswa(nim, nama))
