from flask import Blueprint
from flask import render_template

from BankManager.auth import login_required

bp = Blueprint("link", __name__)
@login_required
@bp.route("/link<string:name>", methods=('GET', 'POST'))
def link(name):
    return render_template("link.html", name=name)
