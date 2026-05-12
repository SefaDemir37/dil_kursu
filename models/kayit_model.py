from database import Database


class Kayit:
    """Öğrenci-Kurs kaydını temsil eden OOP sınıfı."""

    def __init__(self, ogrenci_id, kurs_id, sure_ay, baslangic_tarihi, bitis_tarihi, toplam_fiyat, kayit_id=None):
        self.__kayit_id = kayit_id
        self.__ogrenci_id = ogrenci_id
        self.__kurs_id = kurs_id
        self.__sure_ay = int(sure_ay)
        self.__baslangic_tarihi = baslangic_tarihi
        self.__bitis_tarihi = bitis_tarihi
        self.__toplam_fiyat = float(toplam_fiyat)

    @property
    def kayit_id(self):
        return self.__kayit_id

    @property
    def ogrenci_id(self):
        return self.__ogrenci_id

    @property
    def kurs_id(self):
        return self.__kurs_id

    @property
    def sure_ay(self):
        return self.__sure_ay

    @property
    def baslangic_tarihi(self):
        return self.__baslangic_tarihi

    @property
    def bitis_tarihi(self):
        return self.__bitis_tarihi

    @property
    def toplam_fiyat(self):
        return self.__toplam_fiyat

    def to_dict(self):
        return {
            "kayit_id": self.__kayit_id,
            "ogrenci_id": self.__ogrenci_id,
            "kurs_id": self.__kurs_id,
            "sure_ay": self.__sure_ay,
            "baslangic_tarihi": self.__baslangic_tarihi,
            "bitis_tarihi": self.__bitis_tarihi,
            "toplam_fiyat": self.__toplam_fiyat,
        }


class KayitDAO:
    """Kayıt CRUD işlemlerini veritabanı üzerinden yürüten Data Access Object."""

    def __init__(self):
        self.db = Database()

    def hepsini_getir(self):
        sorgu = """
            SELECT k.kayit_id,
                   o.ad, o.soyad, o.email,
                   kr.kurs_adi, kr.dil, kr.seviye,
                   kr.saatlik_ucret, kr.haftalik_saat,
                   k.sure_ay, k.baslangic_tarihi, k.bitis_tarihi, k.toplam_fiyat
            FROM kayitlar k
            JOIN ogrenciler o  ON k.ogrenci_id = o.ogrenci_id
            JOIN kurslar    kr ON k.kurs_id    = kr.kurs_id
            ORDER BY k.kayit_id DESC
        """
        return self.db.sorgu_calistir(sorgu)

    def id_ile_getir(self, kayit_id):
        sorgu = """
            SELECT k.kayit_id, k.ogrenci_id, k.kurs_id,
                   k.sure_ay, k.baslangic_tarihi, k.bitis_tarihi, k.toplam_fiyat,
                   o.ad, o.soyad, kr.kurs_adi, kr.dil, kr.seviye,
                   kr.saatlik_ucret, kr.haftalik_saat
            FROM kayitlar k
            JOIN ogrenciler o  ON k.ogrenci_id = o.ogrenci_id
            JOIN kurslar    kr ON k.kurs_id    = kr.kurs_id
            WHERE k.kayit_id = %s
        """
        sonuc = self.db.sorgu_calistir(sorgu, (kayit_id,))
        return sonuc[0] if sonuc else None

    def ekle(self, kayit: Kayit):
        return self.db.degisiklik_uygula(
            """INSERT INTO kayitlar
               (ogrenci_id, kurs_id, sure_ay, baslangic_tarihi, bitis_tarihi, toplam_fiyat)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (kayit.ogrenci_id, kayit.kurs_id, kayit.sure_ay,
             kayit.baslangic_tarihi, kayit.bitis_tarihi, kayit.toplam_fiyat),
        )

    def son_kayit_id(self):
        sonuc = self.db.sorgu_calistir("SELECT MAX(kayit_id) as son_id FROM kayitlar")
        return sonuc[0]["son_id"] if sonuc else None

    def sil(self, kayit_id):
        self.db.degisiklik_uygula(
            "DELETE FROM ders_programi WHERE kayit_id = %s", (kayit_id,)
        )
        return self.db.degisiklik_uygula(
            "DELETE FROM kayitlar WHERE kayit_id = %s", (kayit_id,)
        )


class DersProgramiDAO:
    """Ders programı CRUD işlemleri."""

    def __init__(self):
        self.db = Database()

    def hepsini_getir(self):
        sorgu = """
            SELECT dp.program_id, dp.gun, dp.ders_saati,
                   o.ad, o.soyad,
                   kr.kurs_adi, kr.dil, kr.seviye,
                   k.baslangic_tarihi, k.bitis_tarihi, k.kayit_id
            FROM ders_programi dp
            JOIN kayitlar    k  ON dp.kayit_id   = k.kayit_id
            JOIN ogrenciler  o  ON k.ogrenci_id  = o.ogrenci_id
            JOIN kurslar     kr ON k.kurs_id     = kr.kurs_id
            ORDER BY
              FIELD(dp.gun,'Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi','Pazar'),
              dp.ders_saati
        """
        return self.db.sorgu_calistir(sorgu)

    def kayita_gore_getir(self, kayit_id):
        return self.db.sorgu_calistir(
            "SELECT * FROM ders_programi WHERE kayit_id = %s ORDER BY FIELD(gun,'Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi','Pazar'), ders_saati",
            (kayit_id,)
        )

    def ekle(self, kayit_id, gun, ders_saati):
        return self.db.degisiklik_uygula(
            "INSERT INTO ders_programi (kayit_id, gun, ders_saati) VALUES (%s,%s,%s)",
            (kayit_id, gun, ders_saati)
        )

    def sil(self, program_id):
        return self.db.degisiklik_uygula(
            "DELETE FROM ders_programi WHERE program_id = %s", (program_id,)
        )
