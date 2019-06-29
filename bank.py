from flask import Blueprint
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template

from BankManager.db import session_scope
# from BankManager.auth import login_required

from BankManager.query import getBank, newBank, setBank


bp = Blueprint("bank", __name__)
page_length = 10

@bp.route("/", methods=('GET', 'POST'))
def index(page=None):
    return redirect(url_for("bank.bank", page=0))

@bp.route("/bank<int:page>", methods=('GET', 'POST'))
def bank(page=None):
    if not page:
        page = 0
    with session_scope() as session:
        cont = getBank(session)
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        waytosort = request.form['way']
        if waytosort == 'option2':
            with session_scope() as session:
                cont = getBank(session, name=name, city=city)

    return render_template("admin-table.html", page=page, cont=cont, tot=len(cont))

@bp.route("/addbank", methods=('GET', 'POST'))
# @login_required
def addbank():
    if request.method == 'POST':
        print("hello")
        bankname = request.form["bankname"]
        city = request.form["bankcity"]
        property = request.form["property"]
        error = None
        print([bankname, city, property])
        if not bankname:
            error = "Bank Name is required."

        if not city:
            error = "City is required."

        if not property:
            error = "Property is required."

        if error is not None:
            flash(error)
        else:
            with session_scope() as session:
                newBank(session, bankname, city, int(property))
    return render_template("add.html", type=0)
