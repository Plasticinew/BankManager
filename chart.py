from flask import Blueprint
from flask import request
from flask import render_template

bp = Blueprint("chart", __name__)

from BankManager.auth import login_required

@bp.route("/chart", methods=('GET', 'POST'))
@login_required
def chart():
    cont = []
    if request.method == 'POST':
        payid = request.form['payid']
        loanid = request.form['loanid']
        date = request.form['date']
        amount = request.form['amount']
        return render_template("success.html", action="添加", succ=1, showurl=None,
                               message=None)
    return render_template("chart.html", cont=cont)