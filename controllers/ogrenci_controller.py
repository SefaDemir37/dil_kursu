from flask import Blueprint, request, redirect, url_for, flash, render_template
from models import Ogrenci, OgrenciDAO

ogrenci_bp = Blueprint("ogrenci", __name__)
dao = OgrenciDAO()


@ogrenci_bp.route("/")
def listele():
    ogrenciler = dao.hepsini_getir()
    return render_template("ogrenciler.html", ogrenciler=ogrenciler)


@ogrenci_bp.route("/ekle", methods=["GET", "POST"])
def ekle():
    if request.method == "POST":
        o = Ogrenci(
            ad=request.form["ad"],
            soyad=request.form["soyad"],
            email=request.form["email"],
            telefon=request.form["telefon"],
        )
        dao.ekle(o)
        flash("Öğrenci başarıyla eklendi.", "success")
        return redirect(url_for("ogrenci.listele"))
    return render_template("ogrenci_form.html", ogrenci=None, baslik="Öğrenci Ekle")


@ogrenci_bp.route("/guncelle/<int:ogrenci_id>", methods=["GET", "POST"])
def guncelle(ogrenci_id):
    mevcut = dao.id_ile_getir(ogrenci_id)
    if not mevcut:
        flash("Öğrenci bulunamadı.", "danger")
        return redirect(url_for("ogrenci.listele"))

    if request.method == "POST":
        o = Ogrenci(
            ad=request.form["ad"],
            soyad=request.form["soyad"],
            email=request.form["email"],
            telefon=request.form["telefon"],
        )
        dao.guncelle(ogrenci_id, o)
        flash("Öğrenci güncellendi.", "success")
        return redirect(url_for("ogrenci.listele"))

    return render_template("ogrenci_form.html", ogrenci=mevcut, baslik="Öğrenci Güncelle")


@ogrenci_bp.route("/sil/<int:ogrenci_id>", methods=["POST"])
def sil(ogrenci_id):
    dao.sil(ogrenci_id)
    flash("Öğrenci silindi.", "warning")
    return redirect(url_for("ogrenci.listele"))
