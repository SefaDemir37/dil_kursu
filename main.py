from flask import Flask, render_template
from controllers import ogrenci_bp, kurs_bp, kayit_bp, program_bp

app = Flask(__name__)
app.secret_key = "dil_kursu_gizli_anahtar_2025"

# Blueprint kayıtları (modüler yapı)
app.register_blueprint(ogrenci_bp, url_prefix="/ogrenciler")
app.register_blueprint(kurs_bp,    url_prefix="/kurslar")
app.register_blueprint(kayit_bp,   url_prefix="/kayitlar")
app.register_blueprint(program_bp, url_prefix="/program")


@app.route("/")
def anasayfa():
    return render_template("anasayfa.html")


if __name__ == "__main__":
    app.run(debug=True)
