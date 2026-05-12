import mysql.connector
from mysql.connector import Error


class Database:
    """Veritabanı bağlantısını yöneten sınıf."""

    def __init__(self, host="localhost", user="root", password="", db_name="dil_kursu"):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.connection = None

    def baglan(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )
            return self.connection
        except Error as e:
            print(f"Bağlantı hatası: {e}")
            return None

    def kapat(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def sorgu_calistir(self, sorgu, parametreler=None):
        """SELECT sorguları için"""
        baglanti = self.baglan()
        if not baglanti:
            return []
        cursor = baglanti.cursor(dictionary=True)
        cursor.execute(sorgu, parametreler or ())
        sonuc = cursor.fetchall()
        self.kapat()
        return sonuc

    def degisiklik_uygula(self, sorgu, parametreler=None):
        """INSERT / UPDATE / DELETE için"""
        baglanti = self.baglan()
        if not baglanti:
            return False
        cursor = baglanti.cursor()
        cursor.execute(sorgu, parametreler or ())
        baglanti.commit()
        self.kapat()
        return True
