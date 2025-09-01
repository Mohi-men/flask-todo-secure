from flask import redirect, url_for
from . import bp

@bp.route("/")
def home():
    return redirect(url_for("auth.login"))