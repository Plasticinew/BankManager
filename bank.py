from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from BankManager.db import session_scope

from BankManager.auth import login_required

from BankManager.query import getBank, newBank, setBank, delBank

from BankManager.error import flash



with session_scope() as session:
    global cont
    cont = getBank(session)


bp = Blueprint("bank", __name__)
page_length = 10

@bp.route("/", methods=('GET', 'POST'))
@login_required
def index(page=None):
    return redirect(url_for("bank.bank", page=0))
    # return render_template("login.html")

@bp.route("/bank<int:page>", methods=('GET', 'POST'))
@login_required
def bank(page=None):
    global cont
    if not page:
        page = 0
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        waytosort = request.form['way']
        if waytosort == 'option0':
            cont = []
        if waytosort == 'option1':
            with session_scope() as session:
                cont = getBank(session, name=name, city=city, orderby='Property')
        if waytosort == 'option2':
            with session_scope() as session:
                cont = getBank(session, name=name, city=city)
        if waytosort == 'option3':
            with session_scope() as session:
                cont = getBank(session, name=name, city=city, orderby='City')
    return render_template("admin-table.html", page=page, cont=cont, tot=len(cont))

@bp.route("/addbank", methods=('GET', 'POST'))
@login_required
def addbank():
    if request.method == 'POST':
        bankname = request.form["bankname"]
        city = request.form["bankcity"]
        property = request.form["property"]
        error = None
        if bankname == '':
            error = "Bank Name is required."

        if city == '':
            error = "City is required."

        if property == '':
            error = "Property is required."

        if error is not None:
            print(error)
            return flash(error, "增加支行", url_for("bank.bank", page=0))
        else:
            with session_scope() as session:
                newBank(session, bankname, city, int(property))

            with session_scope() as session:
                global cont
                cont = getBank(session)
            return render_template("success.html", action="增加", \
                                   succ=1, showurl=url_for("bank.bank", page=0), messege=None)
    return render_template("add.html", type=2)

@bp.route("/editbank<string:pk>", methods=('GET', 'POST'))
@login_required
def editbank(pk):
    if request.method == 'POST':
        city = request.form['bankcity']
        property = request.form['property']
        bankname = request.form['bankname']

        with session_scope() as session:

            if bankname:
                try:
                    setBank(session, pk, bankname, 'BankName')
                except Exception as e:
                    error = e.args[0]
                    return flash(error, "修改支行信息", url_for("bank.bank", page=0))
                pk = bankname

            if city:
                setBank(session, pk, city, 'City')

            if property:
                setBank(session, pk, property, 'Property')

        with session_scope() as session:
            global cont
            cont = getBank(session)
        return render_template("success.html", action="编辑", \
                               succ=1, showurl=url_for("bank.bank", page=0), messege=None)

    return render_template("edit.html", type=2)

@bp.route("/delbank<string:pk>", methods=('GET', 'POST'))
@login_required
def delbank(pk):
    with session_scope() as session:
        try:
            delBank(session, pk)
        except Exception as e:
            error = e.args[0]
            return flash(error, "删除支行信息", url_for("bank.bank", page=0))
    return render_template("del.html", type=2, succ=1)

@bp.route("/success<string:p>", methods=('GET', 'POST'))
def success(p):
    return render_template("success.html", action="保存", \
                           succ=1, showurl=url_for(p + '.' + p, page=0), messege=None)