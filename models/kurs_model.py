from database import Database


class Kurs:
    """Kurs verilerini temsil eden OOP sınıfı."""

    def __init__(self, kurs_adi, dil, seviye, saatlik_ucret, haftalik_saat, kurs_id=None):
        self.__kurs_id = kurs_id
        self.__kurs_adi = kurs_adi
        self.__dil = dil
        self.__seviye = seviye
        self.__saatlik_ucret = float(saatlik_ucret)
        self.__haftalik_saat = int(haftalik_saat)

    @property
    def kurs_id(self):
        return self.__kurs_id

    @property
    def kurs_adi(self):
        return self.__kurs_adi

    @kurs_adi.setter
    def kurs_adi(self, deger):
        self.__kurs_adi = deger

    @property
    def dil(self):
        return self.__dil

    @dil.setter
    def dil(self, deger):
        self.__dil = deger

    @property
    def seviye(self):
        return self.__seviye

    @seviye.setter
    def seviye(self, deger):
        self.__seviye = deger

    @property
    def saatlik_ucret(self):
        return self.__saatlik_ucret

    @saatlik_ucret.setter
    def saatlik_ucret(self, deger):
        self.__saatlik_ucret = float(deger)

    @property
    def haftalik_saat(self):
        return self.__haftalik_saat

    @haftalik_saat.setter
    def haftalik_saat(self, deger):
        self.__haftalik_saat = int(deger)

    def aylik_ucret_hesapla(self):
        """1 ay = 4 hafta olarak hesaplar."""
        return self.__saatlik_ucret * self.__haftalik_saat * 4

    def toplam_ucret_hesapla(self, sure_ay):
        """Verilen ay sayısına göre toplam ücreti hesaplar."""
        return self.aylik_ucret_hesapla() * sure_ay

    def to_dict(self):
        return {
            "kurs_id": self.__kurs_id,
            "kurs_adi": self.__kurs_adi,
            "dil": self.__dil,
            "seviye": self.__seviye,
            "saatlik_ucret": self.__saatlik_ucret,
            "haftalik_saat": self.__haftalik_saat,
        }


class KursDAO:
    """Kurs CRUD işlemlerini veritabanı üzerinden yürüten Data Access Object."""

    def __init__(self):
        self.db = Database()

    def hepsini_getir(self):
        return self.db.sorgu_calistir("SELECT * FROM kurslar ORDER BY kurs_id DESC")

    def id_ile_getir(self, kurs_id):
        sonuc = self.db.sorgu_calistir(
            "SELECT * FROM kurslar WHERE kurs_id = %s", (kurs_id,)
        )
        return sonuc[0] if sonuc else None

    def ekle(self, kurs: Kurs):
        return self.db.degisiklik_uygula(
            "INSERT INTO kurslar (kurs_adi, dil, seviye, saatlik_ucret, haftalik_saat) VALUES (%s,%s,%s,%s,%s)",
            (kurs.kurs_adi, kurs.dil, kurs.seviye, kurs.saatlik_ucret, kurs.haftalik_saat),
        )

    def guncelle(self, kurs_id, kurs: Kurs):
        return self.db.degisiklik_uygula(
            "UPDATE kurslar SET kurs_adi=%s, dil=%s, seviye=%s, saatlik_ucret=%s, haftalik_saat=%s WHERE kurs_id=%s",
            (kurs.kurs_adi, kurs.dil, kurs.seviye, kurs.saatlik_ucret, kurs.haftalik_saat, kurs_id),
        )

    def sil(self, kurs_id):
        self.db.degisiklik_uygula(
            "DELETE FROM ders_programi WHERE kayit_id IN (SELECT kayit_id FROM kayitlar WHERE kurs_id=%s)", (kurs_id,)
        )
        self.db.degisiklik_uygula(
            "DELETE FROM kayitlar WHERE kurs_id = %s", (kurs_id,)
        )
        return self.db.degisiklik_uygula(
            "DELETE FROM kurslar WHERE kurs_id = %s", (kurs_id,)
        )
