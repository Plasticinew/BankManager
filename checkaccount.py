from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for

from BankManager.auth import login_required
from BankManager.db import session_scope
from BankManager.query import getCheckAccount, newCheckAccount,\
    setAccount_balance, setAccount_others, delAccount

from BankManager.error import flash

with session_scope() as session:
    global cont
    cont = getCheckAccount(session)

bp = Blueprint("checkaccount", __name__)

@bp.route("/checkaccount<int:page>", methods=('GET', 'POST'))
@login_required
def checkaccount(page=None):
    global cont

    if not page:
        page = 0

    if request.method == 'POST':
        accountid = request.form['checkaccountid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        waytosort = request.form['way']

        if waytosort == 'option0':
            cont = []

        if waytosort == 'option1':
            with session_scope() as session:
                cont = getCheckAccount(session, accountid=account,\
                       clientid=clientid, clientname=clientname, bank=bankname, orderby="CheckAccountID")

        if waytosort == 'option2':
            with session_scope() as session:
                cont = getCheckAccount(session, accountid=accountid,\
                clientid=clientid, clientname=clientname, bank=bankname, orderby="ClientID")

        if waytosort == 'option3':
            cont = []
            with session_scope() as session:
                cont = getCheckAccount(session, accountid=accountid,\
                clientid=clientid, clientname=clientname, bank=bankname)
                cont = sorted(cont, key=lambda x: x[3])

    return render_template("checkaccount-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/addcheckaccount", methods=('GET', 'POST'))
@login_required
def addcheckaccount():
    if request.method == 'POST':

        error = None

        accountid = request.form['accountid']

        if not accountid:
            error = "必须填写支票账户ID!"

        bankname = request.form['bankname']

        if not bankname:
            error = "必须填写支行名称!"

        clientid = request.form['clientid']

        if not clientid:
            error = "必须填写客户ID!"

        balance = request.form['balance']

        if not balance:
            error = "必须填写账户余额!"

        dateopening = request.form['dateopening']

        if not dateopening:
            error = "必须填写开户日期"

        overdraft = request.form['overdraft']

        if not overdraft:
            error = "必须填写透支额度"

        if error is not None:
            print(error)
            return flash(error, "添加支票账户", url_for("checkaccount.checkaccount", page=0))
        else:
            with session_scope() as session:
                try:
                    newCheckAccount(session, accountid, clientid, bankname, balance,\
                                    dateopening, overdraft)
                except Exception as e:
                    error = e.args[0]
                    return flash(error, "添加支票账户", url_for("checkaccount.checkaccount", page=0))

            with session_scope() as session:
                global cont
                cont = getCheckAccount(session)

        return render_template("success.html", action="添加", succ=1, showurl=url_for("checkaccount.checkaccount", page=0),
                               message=None)
    return render_template("edit.html", type=4)


@bp.route("/editcheckaccount<string:pk>", methods=('GET', 'POST'))
@login_required
def editcheckaccount(pk):
    if request.method == 'POST':
        accountid = request.form['accountid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        balance = request.form['balance']
        dateopening = request.form['dateopening']
        overdraft = request.form['overdraft']

        with session_scope() as session:

            if accountid:
                error = "不允许修改支票账户ID!"
                return flash(error, "修改支票账户", url_for("checkaccount.checkaccount", page=0))

            if bankname:
                setAccount_others(session, pk, bankname, "BankName")

            if clientid:
                setAccount_others(session, pk, clientid, "ClientID")

            if balance:
                if dateopening:
                    setAccount_balance(session, pk, float(balance), dateopening)
                else:
                    error = "必须填写余额变动日期!"
                    return flash(error, "修改支票账户", url_for("checkaccount.checkaccount", page=0))

            if dateopening:
                setAccount_others(session, pk, dateopening, "DateOpening")

            if overdraft:
                setAccount_others(session, pk, overdraft, "OverDraft")

        with session_scope() as session:
            cont = getCheckAccount(session)

        return render_template("success.html", action="修改", succ=1, showurl=url_for("checkaccount.checkaccount", page=0), message=None)
    return render_template("edit.html", type=4)


@bp.route("/delcheckaccount<string:pk>", methods=('GET', 'POST'))
@login_required
def delcheckaccount(pk):
    with session_scope() as session:
        try:
            delAccount(session, pk)
        except Exception as e:
            error = e.args[0]
            return flash(error, "删除支票账户", url_for("checkaccount.checkaccount", page=0))

    with session_scope() as session:
        global cont
        cont = getCheckAccount(session)

    return render_template("success.html", action="删除", succ=1, showurl=url_for("checkaccount.checkaccount", page=0), message=None)
