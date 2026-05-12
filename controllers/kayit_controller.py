from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from models import Kayit, KayitDAO, OgrenciDAO, KursDAO, DersProgramiDAO

kayit_bp = Blueprint("kayit", __name__)
kayit_dao    = KayitDAO()
ogrenci_dao  = OgrenciDAO()
kurs_dao     = KursDAO()
program_dao  = DersProgramiDAO()

GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]


@kayit_bp.route("/")
def listele():
    kayitlar = kayit_dao.hepsini_getir()
    return render_template("kayitlar.html", kayitlar=kayitlar)


@kayit_bp.route("/ekle", methods=["GET", "POST"])
def ekle():
    if request.method == "POST":
        kurs_id       = request.form["kurs_id"]
        sure_ay       = int(request.form["sure_ay"])
        baslangic_str = request.form["baslangic_tarihi"]

        # Bitiş tarihini otomatik hesapla
        baslangic     = date.fromisoformat(baslangic_str)
        bitis         = baslangic + relativedelta(months=sure_ay)

        # Toplam fiyatı otomatik hesapla
        kurs          = kurs_dao.id_ile_getir(kurs_id)
        toplam_fiyat  = float(kurs["saatlik_ucret"]) * int(kurs["haftalik_saat"]) * 4 * sure_ay

        k = Kayit(
            ogrenci_id       = request.form["ogrenci_id"],
            kurs_id          = kurs_id,
            sure_ay          = sure_ay,
            baslangic_tarihi = baslangic_str,
            bitis_tarihi     = bitis.isoformat(),
            toplam_fiyat     = toplam_fiyat,
        )
        kayit_dao.ekle(k)

        # Ders programını kaydet
        secilen_gunler = request.form.getlist("gunler")
        ders_saati     = request.form["ders_saati"]
        kayit_id       = kayit_dao.son_kayit_id()
        for gun in secilen_gunler:
            program_dao.ekle(kayit_id, gun, ders_saati)

        flash("Öğrenci kursa kaydedildi.", "success")
        return redirect(url_for("kayit.listele"))

    ogrenciler = ogrenci_dao.hepsini_getir()
    kurslar    = kurs_dao.hepsini_getir()
    return render_template("kayit_form.html",
                           ogrenciler=ogrenciler,
                           kurslar=kurslar,
                           gunler=GUNLER)


@kayit_bp.route("/fiyat_hesapla")
def fiyat_hesapla():
    """AJAX ile anlık fiyat hesaplama."""
    kurs_id  = request.args.get("kurs_id")
    sure_ay  = request.args.get("sure_ay", type=int)
    if not kurs_id or not sure_ay:
        return jsonify({"fiyat": 0})
    kurs = kurs_dao.id_ile_getir(kurs_id)
    if not kurs:
        return jsonify({"fiyat": 0})
    toplam = float(kurs["saatlik_ucret"]) * int(kurs["haftalik_saat"]) * 4 * sure_ay
    aylik  = float(kurs["saatlik_ucret"]) * int(kurs["haftalik_saat"]) * 4
    return jsonify({
        "fiyat": toplam,
        "aylik": aylik,
        "haftalik_saat": kurs["haftalik_saat"],
        "saatlik_ucret": kurs["saatlik_ucret"],
    })


@kayit_bp.route("/sil/<int:kayit_id>", methods=["POST"])
def sil(kayit_id):
    kayit_dao.sil(kayit_id)
    flash("Kayıt silindi.", "warning")
    return redirect(url_for("kayit.listele"))
