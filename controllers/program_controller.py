from flask import Blueprint, render_template
from models import DersProgramiDAO

program_bp  = Blueprint("program", __name__)
program_dao = DersProgramiDAO()

GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]


@program_bp.route("/")
def listele():
    dersler = program_dao.hepsini_getir()
    # Günlere göre grupla
    programa_gore = {gun: [] for gun in GUNLER}
    for ders in dersler:
        gun = ders["gun"]
        if gun in programa_gore:
            programa_gore[gun].append(ders)
    return render_template("ders_programi.html", programa_gore=programa_gore, gunler=GUNLER)
