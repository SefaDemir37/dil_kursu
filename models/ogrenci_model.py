from database import Database


class Ogrenci:
    """Öğrenci verilerini temsil eden OOP sınıfı."""

    def __init__(self, ad, soyad, email, telefon, ogrenci_id=None):
        self.__ogrenci_id = ogrenci_id   # Kapsülleme (private)
        self.__ad = ad
        self.__soyad = soyad
        self.__email = email
        self.__telefon = telefon

    # --- Getter / Setter (Kapsülleme) ---
    @property
    def ogrenci_id(self):
        return self.__ogrenci_id

    @property
    def ad(self):
        return self.__ad

    @ad.setter
    def ad(self, yeni_ad):
        self.__ad = yeni_ad

    @property
    def soyad(self):
        return self.__soyad

    @soyad.setter
    def soyad(self, yeni_soyad):
        self.__soyad = yeni_soyad

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, yeni_email):
        self.__email = yeni_email

    @property
    def telefon(self):
        return self.__telefon

    @telefon.setter
    def telefon(self, yeni_telefon):
        self.__telefon = yeni_telefon

    def to_dict(self):
        return {
            "ogrenci_id": self.__ogrenci_id,
            "ad": self.__ad,
            "soyad": self.__soyad,
            "email": self.__email,
            "telefon": self.__telefon,
        }


class OgrenciDAO:
    """Öğrenci CRUD işlemlerini veritabanı üzerinden yürüten Data Access Object."""

    def __init__(self):
        self.db = Database()

    def hepsini_getir(self):
        return self.db.sorgu_calistir("SELECT * FROM ogrenciler ORDER BY ogrenci_id DESC")

    def id_ile_getir(self, ogrenci_id):
        sonuc = self.db.sorgu_calistir(
            "SELECT * FROM ogrenciler WHERE ogrenci_id = %s", (ogrenci_id,)
        )
        return sonuc[0] if sonuc else None

    def ekle(self, ogrenci: Ogrenci):
        return self.db.degisiklik_uygula(
            "INSERT INTO ogrenciler (ad, soyad, email, telefon) VALUES (%s, %s, %s, %s)",
            (ogrenci.ad, ogrenci.soyad, ogrenci.email, ogrenci.telefon),
        )

    def guncelle(self, ogrenci_id, ogrenci: Ogrenci):
        return self.db.degisiklik_uygula(
            "UPDATE ogrenciler SET ad=%s, soyad=%s, email=%s, telefon=%s WHERE ogrenci_id=%s",
            (ogrenci.ad, ogrenci.soyad, ogrenci.email, ogrenci.telefon, ogrenci_id),
        )

    def sil(self, ogrenci_id):
        # Önce kayıtları temizle (foreign key)
        self.db.degisiklik_uygula(
            "DELETE FROM kayitlar WHERE ogrenci_id = %s", (ogrenci_id,)
        )
        return self.db.degisiklik_uygula(
            "DELETE FROM ogrenciler WHERE ogrenci_id = %s", (ogrenci_id,)
        )
