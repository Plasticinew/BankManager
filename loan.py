from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for

from BankManager.auth import login_required
from BankManager.db import session_scope
from BankManager.query import getLoan, getPay, newLoan, delLoan, addPay

from BankManager.error import flash

with session_scope() as session:
    global cont
    cont = getLoan(session)

bp = Blueprint("loan", __name__)

@bp.route("/loan<int:page>", methods=('GET', 'POST'))
@login_required
def loan(page=None):
    global cont

    if not page:
        page = 0

    if request.method == 'POST':
        loanid = request.form['loanid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        waytosort = request.form['way']

        if waytosort == 'option0':
            cont = []

        if waytosort == 'option1':
            pass

    return render_template("loan-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/detailedloan<int:loanid>", methods=('GET', 'POST'))
@login_required
def detailedloan(loanid=None):

    cont = [['1', '2', '100'],
            ['2', '3', '1000'],
            ['3', '4', '10000']
            ]

    if request.method == 'POST':
        loanid = request.form['loanid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        waytosort = request.form['way']

    return render_template("detailedloan-table.html", cont=cont, tot=len(cont))


@bp.route("/addloan", methods=('GET', 'POST'))
@login_required
def addloan():
    if request.method == 'POST':
        loanid = request.form['loanid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        amount = request.form['amount']
        return render_template("success.html", action="添加", succ=1, showurl=url_for("bank.loan", page=0),
                               message=None)
    return render_template("edit.html", type=5)


@bp.route("/delloan<string:pk>", methods=('GET', 'POST'))
@login_required
def delloan(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.loan", page=0), message=None)


@bp.route("/addpay", methods=('GET', 'POST'))
@login_required
def addpay():
    if request.method == 'POST':
        payid = request.form['payid']
        loanid = request.form['loanid']
        date = request.form['date']
        amount = request.form['amount']
        return render_template("success.html", action="添加", succ=1, showurl=None,
                               message=None)
    return render_template("edit.html", type=6)


@bp.route("/delpay<string:pk>", methods=('GET', 'POST'))
@login_required
def delpay(pk):
    return render_template("success.html", action="删除", succ=1, showurl=None, message=None)
