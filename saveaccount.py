from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for

from BankManager.auth import login_required
from BankManager.db import session_scope
from BankManager.query import getSaveAccount, newSaveAccount,\
    setAccount_balance, setAccount_others, delAccount
from BankManager.error import flash

with session_scope() as session:
    global cont
    cont = getSaveAccount(session)

bp = Blueprint("saveaccount", __name__)

@bp.route("/saveaccount<int:page>", methods=('GET', 'POST'))
@login_required
def saveaccount(page=None):
    global cont

    if not page:
        page = 0

    if request.method == 'POST':
        accountid = request.form['saveaccountid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        waytosort = request.form['way']
        if waytosort == 'option0':
            cont = []
        if waytosort == 'option1':
            with session_scope() as session:
                cont = getSaveAccount(session, accountid=accountid, \
                                      clientid=clientid, clientname=clientname, \
                                      bank=bankname)
        if waytosort == 'option2':
            with session_scope() as session:
                cont = getSaveAccount(session, accountid=accountid, \
                                      clientid=clientid, clientname=clientname, \
                                      bank=bankname, orderby="ClientID")
        if waytosort == 'option3':
            cont = []
            # TODO:客户id
            # with session_scope() as session:
            #     cont = getSaveAccount(session, accountid=accountid, \
            #                           clientid=clientid, clientname=clientname, \
            #                           bank=bankname, orderby="ClientName")j

    return render_template("saveaccount-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/addsaveaccount", methods=('GET', 'POST'))
@login_required
def addsaveaccount():
    if request.method == 'POST':

        error = None

        accountid = request.form['accountid']

        if not accountid:
            error = "Saving Account ID is required."

        bankname = request.form['bankname']

        if not bankname:
            error = "Bank Name is required."

        clientid = request.form['clientid']

        if not clientid:
            error = "Client ID is required."

        balance = request.form['balance']

        if not balance:
            error = "Account Balance is required."

        dateopening = request.form['dateopening']

        if not dateopening:
            error = "Account opening date is required."

        rate = request.form['rate']

        if not rate:
            error = "Interest Rate is required."

        moneytype = request.form['moneytype']

        if not moneytype:
            error = "Currency is required."

        if error is not None:
            print(error)
            return flash(error, "添加储蓄账户", url_for("saveaccount.saveaccount", page=0))
        else:
            with session_scope() as session:
                try:
                    newSaveAccount(session, accountid, clientid, bankname, balance, dateopening,\
                            rate, moneytype)
                except Exception as e:
                    error = e.args[0]
                    print(error)
                    return flash(error, "添加储蓄账户", url_for("saveaccount.saveaccount", page=0))

            with session_scope() as session:
                global cont
                cont = getSaveAccount(session)

            return render_template("success.html", action="添加", succ=1, showurl=url_for("saveaccount.saveaccount", page=0),
                               message=None)

    return render_template("edit.html", type=0)


@bp.route("/editsaveaccount<string:pk>", methods=('GET', 'POST'))
@login_required
def editsaveaccount(pk):
    if request.method == 'POST':
        global cont
        accountid = request.form['accountid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        balance = request.form['balance']
        dateopening = request.form['dateopening']
        rate = request.form['rate']
        moneytype = request.form['moneytype']

        with session_scope() as session:
            if accountid:
                try:
                    setAccount_others(session, pk, accountid, "AccountID")
                except Exception as e:
                    error = e.args[0]
                    return flash(error, "编辑储蓄账户", url_for("saveaccount.saveaccount", page=0))

            if bankname:
                setAccount_others(session, pk, bankname, "BankName")

            if clientid:
                setAccount_others(session, pk, clientid, "ClientID")

            if balance:
                if dateopening:
                    setAccount_balance(session, pk, float(balance), dateopening)
                else:
                    error = "Date is required!"
                    return flash(error, "编辑储蓄账户", url_for("saveaccount.saveaccount", page=0))

            if dateopening:
                setAccount_others(session, pk, dateopening, "DateOpening")

            if rate:
                setAccount_others(session, pk, rate, "Rate")

            if moneytype:
                setAccount_others(session, pk, moneytype, "MoneyType")

        with session_scope() as session:
            cont = getSaveAccount(session)

        return render_template("success.html", action="修改", succ=1, showurl=url_for("saveaccount.saveaccount", page=0), message=None)
    return render_template("edit.html", type=0)


@bp.route("/delsaveaccount<string:pk>", methods=('GET', 'POST'))
@login_required
def delsaveaccount(pk):
    with session_scope() as session:
        try:
            delAccount(session, pk)
        except Exception as e:
            error = e.args[0]
            return flash(error, "删除储蓄账户", url_for("saveaccount.saveaccount", page=0))
    with session_scope() as session:
        global cont
        cont = getSaveAccount(session)
    return render_template("success.html", action="删除", succ=1, showurl=url_for("saveaccount.saveaccount", page=0), message=None)

