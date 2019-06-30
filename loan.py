from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for

from BankManager.auth import login_required
from BankManager.db import session_scope, LoanClass, OwningClass, ClientClass
from BankManager.query import getLoan, getPay, newLoan, delLoan, addPay, getClient,\
    addPay

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
            # Loan ID
            with session_scope() as session:
                cont = getLoan(session, loanid, clientid, clientname, bankname)
                cont = sorted(cont, key=lambda x: x[0])

        if waytosort == 'option2':
            # Client Name
            with session_scope() as session:
                cont = getLoan(session, loanid, clientid, clientname, bankname)
                cont = sorted(cont, key=lambda x: x[2])

        if waytosort == 'option3':
            # Bank Name
            with session_scope() as session:
                cont = getLoan(session, loanid, clientid, clientname, bankname)
                cont = sorted(cont, key=lambda x: x[3])

    return render_template("loan-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/detailedloan<int:loanid>", methods=('GET', 'POST'))
@login_required
def detailedloan(loanid=None):

    global cont, namelist

    with session_scope() as session:
        cont = getPay(session, loanid)
        namelist = '; '.join([client.ClientName for loan, own, client in\
                    session.query(LoanClass, OwningClass, ClientClass).filter(\
                    LoanClass.LoanID == loanid,
                    ClientClass.ClientID == OwningClass.ClientID,
                    LoanClass.LoanID == OwningClass.LoanID,
                    )])

    if request.method == 'POST':
        with session_scope() as session:
            cont = getPay(session, loanid)

        # loanid = request.form['loanid']
        # bankname = request.form['bankname']
        # clientid = request.form['clientid']
        # clientname = request.form['clientname']
        # waytosort = request.form['way']


    return render_template("detailedloan-table.html", cont=cont, tot=len(cont), namelist=namelist)


@bp.route("/addloan", methods=('GET', 'POST'))
@login_required
def addloan():
    if request.method == 'POST':
        error = None

        loanid = request.form['loanid']

        if not loanid:
            error = "必须填写贷款ID!"

        bankname = request.form['bankname']

        if not bankname:
            error = "必须填写支行名称!"

        clientid_list = request.form['clientid'].split(';')


        if not clientid_list:
            error = "必须填写客户ID!"

        amount = request.form['amount']

        if not amount:
            error = "必须填写贷款金额!"

        if error is not None:
            return flash(error, "添加贷款", url_for("loan.loan", page=0))
        else:
            with session_scope() as session:
                newLoan(session, loanid, clientid_list, bankname, amount)

            with session_scope() as session:
                global cont
                cont = getLoan(session)
        return render_template("success.html", action="添加", succ=1, showurl=url_for("loan.loan", page=0),
                               message=None)
    return render_template("edit.html", type=5)


@bp.route("/delloan<string:pk>", methods=('GET', 'POST'))
@login_required
def delloan(pk):
    with session_scope() as session:
        delLoan(session, pk)

    with session_scope() as session:
        global cont
        cont = getLoan(session)

    return render_template("success.html", action="删除", succ=1, showurl=url_for("loan.loan", page=0), message=None)


@bp.route("/addpay", methods=('GET', 'POST'))
@login_required
def addpay():
    if request.method == 'POST':

        error = None

        payid = request.form['payid']

        if not payid:
            error = "必须填写支付ID!"

        loanid = request.form['loanid']

        if not loanid:
            error = "必须填写贷款ID!"

        date = request.form['date']

        if not date:
            error = "必须填写日期!"

        amount = request.form['amount']

        if not amount:
            error = "必须填写金额!"

        if error is not None:
            return flash(error, "新建付款", url_for("loan.loan", page=0))
        else:
            with session_scope() as session:
                addPay(session, payid, loanid, date, amount)

            with session_scope() as session:
                global cont
                cont = getPay(session, loanid)

        return render_template("success.html", action="添加", succ=1, showurl=None,
                               message=None)
    return render_template("edit.html", type=6)


@bp.route("/delpay<string:pk>", methods=('GET', 'POST'))
@login_required
def delpay(pk):
    return render_template("success.html", action="删除", succ=1, showurl=None, message=None)
