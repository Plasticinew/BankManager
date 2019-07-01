from flask import Blueprint
from flask import request
from flask import render_template

from BankManager.query import calculate

from BankManager.db import session_scope
bp = Blueprint("chart", __name__)

from BankManager.auth import login_required

@bp.route("/chart", methods=('GET', 'POST'))
@login_required
def chart():
    with session_scope() as session:
        calculate(session)
    return render_template("chart.html")