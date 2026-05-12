-- ============================================================
-- Dil Kursu Yönetim Sistemi v2 - Veritabanı Kurulum Dosyası
-- phpMyAdmin > dil_kursu seç > İçe Aktar (Import) ile çalıştır
-- ============================================================

USE dil_kursu;

DROP TABLE IF EXISTS ders_programi;
DROP TABLE IF EXISTS kayitlar;
DROP TABLE IF EXISTS kurslar;
DROP TABLE IF EXISTS ogrenciler;

-- ----------------------------
-- Öğrenciler tablosu
-- ----------------------------
CREATE TABLE ogrenciler (
    ogrenci_id INT AUTO_INCREMENT PRIMARY KEY,
    ad         VARCHAR(50)  NOT NULL,
    soyad      VARCHAR(50)  NOT NULL,
    email      VARCHAR(100) NOT NULL UNIQUE,
    telefon    VARCHAR(20)
);

-- ----------------------------
-- Kurslar tablosu
-- ----------------------------
CREATE TABLE kurslar (
    kurs_id        INT AUTO_INCREMENT PRIMARY KEY,
    kurs_adi       VARCHAR(100) NOT NULL,
    dil            VARCHAR(50)  NOT NULL,
    seviye         VARCHAR(5)   NOT NULL,
    saatlik_ucret  DECIMAL(8,2) NOT NULL,
    haftalik_saat  INT          NOT NULL DEFAULT 2
);

-- ----------------------------
-- Kayıtlar tablosu
-- ----------------------------
CREATE TABLE kayitlar (
    kayit_id         INT AUTO_INCREMENT PRIMARY KEY,
    ogrenci_id       INT           NOT NULL,
    kurs_id          INT           NOT NULL,
    sure_ay          INT           NOT NULL,
    baslangic_tarihi DATE          NOT NULL,
    bitis_tarihi     DATE          NOT NULL,
    toplam_fiyat     DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(ogrenci_id),
    FOREIGN KEY (kurs_id)    REFERENCES kurslar(kurs_id)
);

-- ----------------------------
-- Ders Programı tablosu
-- ----------------------------
CREATE TABLE ders_programi (
    program_id INT AUTO_INCREMENT PRIMARY KEY,
    kayit_id   INT         NOT NULL,
    gun        VARCHAR(15) NOT NULL,
    ders_saati TIME        NOT NULL,
    FOREIGN KEY (kayit_id) REFERENCES kayitlar(kayit_id)
);

-- ----------------------------
-- Örnek veriler
-- ----------------------------
INSERT INTO ogrenciler (ad, soyad, email, telefon) VALUES
  ('Ahmet',  'Yılmaz', 'ahmet@example.com',  '0501 111 22 33'),
  ('Fatma',  'Kaya',   'fatma@example.com',   '0502 222 33 44'),
  ('Mehmet', 'Demir',  'mehmet@example.com',  '0503 333 44 55');

INSERT INTO kurslar (kurs_adi, dil, seviye, saatlik_ucret, haftalik_saat) VALUES
  ('Başlangıç İngilizcesi', 'İngilizce', 'A1', 150.00, 2),
  ('Orta Almanca',          'Almanca',   'B1', 200.00, 3),
  ('İleri Fransızca',       'Fransızca', 'C1', 250.00, 2);
