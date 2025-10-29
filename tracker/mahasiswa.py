"""Model Mahasiswa + enkapsulasi presensi."""

class Mahasiswa:
    """Mewakili entitas mahasiswa dengan NIM, nama, dan persentase kehadiran."""

    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        self._hadir_persen = 0.0  # gunakan property untuk akses

    @property
    def hadir_persen(self):
        """Persentase hadir 0..100 (float)."""
        return self._hadir_persen

    @hadir_persen.setter
    def hadir_persen(self, v):
        try:
            v = float(v)
        except Exception:
            raise ValueError("hadir_persen harus angka")
        if v < 0 or v > 100:
            raise ValueError("hadir_persen harus 0..100")
        self._hadir_persen = v

    def info(self):
        """Profil singkat mahasiswa."""
        return "Mahasiswa {} ({}) hadir={:.2f}%".format(self.nama, self.nim, self.hadir_persen)

    def __repr__(self):
        return "<Mahasiswa {} {} hadir={:.2f}%>".format(self.nim, self.nama, self.hadir_persen)
