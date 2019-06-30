from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort


bp = Blueprint("bank", __name__)


@bp.route("/bank<int:page>", methods=('GET', 'POST'))
def bank(page=None):
    if not page:
        page = 0


    cont = [['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['aa', 'aaa', '100'],
            ['aa', 'aaa', '100'],
            ['aa', 'aaa', '100'],
            ['aa', 'aaa', '100'],
            ['aa', 'aaa', '100'],
            ['aa', 'aaa', '100'],
            ['aa', 'aaa', '100'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000']
            ]

    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        minp = request.form['minp']
        maxp = request.form['maxp']
        waytosort = request.form['way']
        cont = [[name, city, waytosort]]

    return render_template("admin-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/staff<int:page>", methods=('GET', 'POST'))
def staff(page=None):
    if not page:
        page = 0

    cont = [['aa', 'aaa', '100', '111', '3423', '3223'],
            ['bb', 'bbb', '1000', 'bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000', 'cc', 'ccc', '10000']
            ]

    if request.method == 'POST':
        staffid = request.form['staffid']
        bankname = request.form['bankname']
        staffname = request.form['staffname']
        phone = request.form['phone']
        minp = request.form['mindate']
        maxp = request.form['maxdate']
        waytosort = request.form['way']

    return render_template("staff-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/addstaff", methods=('GET', 'POST'))
def addstaff():
    if request.method == 'POST':
        staffid = request.form['staffid']
        bankname = request.form['bankname']
        staffname = request.form['staffname']
        address = request.form['address']
        phone = request.form['phone']
        datestartworking = request.form['datestartworking']

        return render_template("success.html", action="添加", succ=1, showurl=url_for("bank.staff", page=0),
                               message=None)
    return render_template("edit.html", type=1)


@bp.route("/editstaff<string:pk>", methods=('GET', 'POST'))
def editstaff(pk):
    if request.method == 'POST':
        staffid = request.form['staffid']
        bankname = request.form['bankname']
        staffname = request.form['staffname']
        address = request.form['address']
        phone = request.form['phone']
        datestartworking = request.form['datestartworking']

        return render_template("success.html", action="修改", succ=1, showurl=url_for("bank.staff", page=0), message=None)
    return render_template("edit.html", type=1)


@bp.route("/delstaff<string:pk>", methods=('GET', 'POST'))
def delstaff(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.staff", page=0), message=None)


@bp.route("/addbank", methods=('GET', 'POST'))
def addbank():
    if request.method == 'POST':
        bankname = request.form['bankname']
        bankcity = request.form['bankcity']
        property = request.form['property']
        print([bankname, bankcity, property])
        return render_template("success.html", action="添加", succ=1, showurl=url_for("bank.bank", page=0),
                               message=None)
    return render_template("edit.html", type=2)


@bp.route("/editbank<string:pk>", methods=('GET', 'POST'))
def editbank(pk):
    if request.method == 'POST':
        bankcity = request.form['bankcity']
        property = request.form['property']
        print([pk, bankcity, property])
        return render_template("success.html", action="修改", succ=1, showurl=url_for("bank.bank", page=0), message=None)
    return render_template("edit.html", type=2)


@bp.route("/delbank<string:pk>", methods=('GET', 'POST'))
def delbank(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.bank", page=0), message=None)


@bp.route("/success<string:p>", methods=('GET', 'POST'))
def success(p):
    return render_template("success.html", action="保存", succ=1, showurl=url_for("bank."+p, page=0), message=None)


@bp.route("/", methods=("GET", "POST"))
def index(page=None):
    return redirect(url_for("bank.bank", page=0))
    # return render_template("login.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    return render_template("login.html")


@bp.route("/client<int:page>", methods=('GET', 'POST'))
def client(page=None):
    if not page:
        page = 0

    cont = [['aa', 'aaa', '100', '111', '3423', '3223'],
            ['bb', 'bbb', '1000', 'bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000', 'cc', 'ccc', '10000']
            ]

    if request.method == 'POST':
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        staffid = request.form['staffid']
        staffname = request.form['staffname']
        phone = request.form['phone']
        waytosort = request.form['way']

    return render_template("client-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/addclient", methods=('GET', 'POST'))
def addclient():
    if request.method == 'POST':
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        linkid = request.form['linkid']
        linkname = request.form['linkname']
        address = request.form['address']
        phone = request.form['phone']

        return render_template("success.html", action="添加", succ=1, showurl=url_for("bank.client", page=0),
                               message=None)
    return render_template("edit.html", type=3)


@bp.route("/editclient<string:pk>", methods=('GET', 'POST'))
def editclient(pk):
    if request.method == 'POST':
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        linkid = request.form['linkid']
        linkname = request.form['linkname']
        address = request.form['address']
        phone = request.form['phone']

        return render_template("success.html", action="修改", succ=1, showurl=url_for("bank.client", page=0), message=None)
    return render_template("edit.html", type=3)


@bp.route("/delclient<string:pk>", methods=('GET', 'POST'))
def delclient(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.client", page=0), message=None)


@bp.route("/saveaccount<int:page>", methods=('GET', 'POST'))
def saveaccount(page=None):
    if not page:
        page = 0

    cont = [['aa', 'aaa', '100', '111', '3423', '3223'],
            ['bb', 'bbb', '1000', 'bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000', 'cc', 'ccc', '10000']
            ]

    if request.method == 'POST':
        accountid = request.form['accountid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        waytosort = request.form['way']

    return render_template("saveaccount-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/addsaveaccount", methods=('GET', 'POST'))
def addsaveaccount():
    if request.method == 'POST':
        accountid = request.form['accountid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        balance = request.form['balance']
        dateopening = request.form['dateopening']
        rate = request.form['rate']
        moneytype = request.form['moneytype']

        return render_template("success.html", action="添加", succ=1, showurl=url_for("bank.saveaccount", page=0),
                               message=None)
    return render_template("edit.html", type=0, show=1)


@bp.route("/editsaveaccount<string:pk>", methods=('GET', 'POST'))
def editsaveaccount(pk):
    if request.method == 'POST':
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        balance = request.form['balance']
        dateopening = request.form['dateopening']
        rate = request.form['rate']
        moneytype = request.form['moneytype']

        return render_template("success.html", action="修改", succ=1, showurl=url_for("bank.saveaccount", page=0), message=None)
    return render_template("edit.html", type=0)


@bp.route("/delsaveaccount<string:pk>", methods=('GET', 'POST'))
def delsaveaccount(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.saveaccount", page=0), message=None)


@bp.route("/checkaccount<int:page>", methods=('GET', 'POST'))
def checkaccount(page=None):
    if not page:
        page = 0

    cont = [['aa', 'aaa', '100', '111', '3423', '3223'],
            ['bb', 'bbb', '1000', 'bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000', 'cc', 'ccc', '10000']
            ]

    if request.method == 'POST':
        accountid = request.form['accountid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        waytosort = request.form['way']

    return render_template("checkaccount-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/addcheckaccount", methods=('GET', 'POST'))
def addcheckaccount():
    if request.method == 'POST':
        accountid = request.form['accountid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        balance = request.form['balance']
        dateopening = request.form['dateopening']
        overdraft = request.form['overdraft']

        return render_template("success.html", action="添加", succ=1, showurl=url_for("bank.checkaccount", page=0),
                               message=None)
    return render_template("edit.html", type=4, show=1)


@bp.route("/editcheckaccount<string:pk>", methods=('GET', 'POST'))
def editcheckaccount(pk):
    if request.method == 'POST':
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        balance = request.form['balance']
        dateopening = request.form['dateopening']
        overdraft = request.form['overdraft']

        return render_template("success.html", action="修改", succ=1, showurl=url_for("bank.checkaccount", page=0), message=None)
    return render_template("edit.html", type=4)


@bp.route("/delcheckaccount<string:pk>", methods=('GET', 'POST'))
def delcheckaccount(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.checkaccount", page=0), message=None)


@bp.route("/loan<int:page>", methods=('GET', 'POST'))
def loan(page=None):
    if not page:
        page = 0

    cont = [['1', 'aaa', '100', '111', '3423', '3223'],
            ['2', 'bbb', '1000', 'bb', 'bbb', '1000'],
            ['3', 'ccc', '10000', 'cc', 'ccc', '10000']
            ]

    if request.method == 'POST':
        loanid = request.form['loanid']
        bankname = request.form['bankname']
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        waytosort = request.form['way']

    return render_template("loan-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/detailedloan<int:loanid>", methods=('GET', 'POST'))
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
def delloan(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.loan", page=0), message=None)


@bp.route("/addpay", methods=('GET', 'POST'))
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
def delpay(pk):
    return render_template("success.html", action="删除", succ=1, showurl=None, message=None)

