# 🌐 Dil Kursu Yönetim Sistemi v2

Kastamonu Üniversitesi Tosya MYO — Programlama II Dönem Sonu Projesi

##  Proje Hakkında

Python ve Flask kullanılarak geliştirilmiş, MySQL veritabanı destekli web tabanlı bir **Dil Kursu Yönetim Sistemi**dir. Öğrenci ve kurs kayıtları CRUD işlemleriyle yönetilmekte; kurslar haftalık saat ve saatlik ücret bazında tanımlanmakta; öğrenciler kurslara süre (1/3/6/12 ay) seçerek otomatik fiyat hesaplamasıyla kaydedilmektedir. Ders programı ayrı bir sayfada görüntülenir.

##  Özellikler

- **Öğrenci Yönetimi** → Ekle, güncelle, sil
- **Kurs Yönetimi** → Haftalık saat, saatlik ücret, otomatik aylık fiyat hesaplama
- **Kayıt Sistemi** → Süre seçimi (1/3/6/12 ay), otomatik bitiş tarihi ve toplam fiyat hesaplama
- **Ders Programı** → Günlere göre haftalık ders programı görüntüleme
- **AJAX** → Kayıt formunda anlık fiyat hesaplama

##  Kurulum

### 1. Gereksinimler
```bash
pip install -r requirements.txt
```

### 2. Veritabanı
- phpMyAdmin'i açın.
- Sol menüden `dil_kursu` veritabanını seçin.
- `veritabani.sql` dosyasını **İçe Aktar (Import)** ile çalıştırın.
- `database.py` içindeki `user` ve `password` alanlarını kendi MySQL bilgilerinizle güncelleyin.

### 3. Çalıştırma
```bash
python main.py
```
Tarayıcıda `http://127.0.0.1:5000` adresini açın.

##  Modül Yapısı

```
dil_kursu/
├── main.py                  # Uygulamanın başlangıç noktası (Blueprint kayıtları)
├── database.py              # MySQL bağlantı yönetimi (Database sınıfı)
├── requirements.txt
├── veritabani.sql           # Veritabanı ve örnek veri
├── models/
│   ├── ogrenci_model.py     # Ogrenci + OgrenciDAO sınıfları
│   ├── kurs_model.py        # Kurs + KursDAO sınıfları (haftalık saat, fiyat hesaplama)
│   └── kayit_model.py       # Kayit + KayitDAO + DersProgramiDAO sınıfları
├── controllers/
│   ├── ogrenci_controller.py  # /ogrenciler rotaları
│   ├── kurs_controller.py     # /kurslar rotaları
│   ├── kayit_controller.py    # /kayitlar rotaları + AJAX fiyat hesaplama
│   └── program_controller.py  # /program rotaları (ders programı)
├── templates/               # Jinja2 HTML şablonları
└── static/css/style.css     # Özel CSS
```
##  OOP Yapısı

| Sınıf | Açıklama |
|-------|----------|
| `Database` | Veritabanı bağlantısı ve sorgu çalıştırma |
| `Ogrenci` | Öğrenci veri modeli (kapsülleme, property'ler) |
| `OgrenciDAO` | Öğrenci CRUD işlemleri |
| `Kurs` | Kurs veri modeli + fiyat hesaplama metodları |
| `KursDAO` | Kurs CRUD işlemleri |
| `Kayit` | Öğrenci-Kurs kaydı modeli (süre, başlangıç/bitiş, fiyat) |
| `KayitDAO` | Kayıt CRUD + JOIN sorguları |
| `DersProgramiDAO` | Ders programı CRUD işlemleri |

##  Teknolojiler

- **Python 3.x** — Ana programlama dili
- **Flask** — Web framework (Blueprint ile modüler yapı)
- **MySQL / phpMyAdmin** — Veritabanı
- **Bootstrap 5** — Arayüz
- **Jinja2** — HTML şablon motoru
- **AJAX / JavaScript** — Anlık fiyat hesaplama

## Veritabanı Şeması

- **ogrenciler** → Öğrenci bilgileri
- **kurslar** → Kurs adı, dil, seviye, saatlik ücret, haftalık saat
- **kayitlar** → Öğrenci-kurs bağlantısı, süre, başlangıç/bitiş tarihi, toplam fiyat
- **ders_programi** → Kayıt bazında hangi günler, hangi saatlerde ders var
