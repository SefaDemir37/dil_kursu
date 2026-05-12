from flask import Blueprint, request, redirect, url_for, flash, render_template
from models import Kurs, KursDAO

kurs_bp = Blueprint("kurs", __name__)
dao = KursDAO()


@kurs_bp.route("/")
def listele():
    kurslar = dao.hepsini_getir()
    return render_template("kurslar.html", kurslar=kurslar)


@kurs_bp.route("/ekle", methods=["GET", "POST"])
def ekle():
    if request.method == "POST":
        k = Kurs(
            kurs_adi=request.form["kurs_adi"],
            dil=request.form["dil"],
            seviye=request.form["seviye"],
            saatlik_ucret=request.form["saatlik_ucret"],
            haftalik_saat=request.form["haftalik_saat"],
        )
        dao.ekle(k)
        flash("Kurs başarıyla eklendi.", "success")
        return redirect(url_for("kurs.listele"))
    return render_template("kurs_form.html", kurs=None, baslik="Kurs Ekle")


@kurs_bp.route("/guncelle/<int:kurs_id>", methods=["GET", "POST"])
def guncelle(kurs_id):
    mevcut = dao.id_ile_getir(kurs_id)
    if not mevcut:
        flash("Kurs bulunamadı.", "danger")
        return redirect(url_for("kurs.listele"))

    if request.method == "POST":
        k = Kurs(
            kurs_adi=request.form["kurs_adi"],
            dil=request.form["dil"],
            seviye=request.form["seviye"],
            saatlik_ucret=request.form["saatlik_ucret"],
            haftalik_saat=request.form["haftalik_saat"],
        )
        dao.guncelle(kurs_id, k)
        flash("Kurs güncellendi.", "success")
        return redirect(url_for("kurs.listele"))

    return render_template("kurs_form.html", kurs=mevcut, baslik="Kurs Güncelle")


@kurs_bp.route("/sil/<int:kurs_id>", methods=["POST"])
def sil(kurs_id):
    dao.sil(kurs_id)
    flash("Kurs silindi.", "warning")
    return redirect(url_for("kurs.listele"))
