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


@bp.route("/stuff<int:page>", methods=('GET', 'POST'))
def stuff(page=None):
    if not page:
        page = 0

    cont = [['aa', 'aaa', '100', '111', '3423', '3223'],
            ['bb', 'bbb', '1000', 'bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000', 'cc', 'ccc', '10000']
            ]

    if request.method == 'POST':
        stuffid = request.form['stuffid']
        bankname = request.form['bankname']
        stuffname = request.form['stuffname']
        phone = request.form['phone']
        minp = request.form['mindate']
        maxp = request.form['maxdate']
        waytosort = request.form['way']

    return render_template("stuff-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/addstuff", methods=('GET', 'POST'))
def addstuff():
    if request.method == 'POST':
        stuffid = request.form['stuffid']
        bankname = request.form['bankname']
        stuffname = request.form['stuffname']
        address = request.form['address']
        phone = request.form['phone']
        datestartworking = request.form['datestartworking']

        return render_template("success.html", action="添加", succ=1, showurl=url_for("bank.stuff", page=0),
                               messege=None)
    return render_template("add.html", type=1)


@bp.route("/editstuff<string:pk>", methods=('GET', 'POST'))
def editstuff(pk):
    if request.method == 'POST':
        stuffid = request.form['stuffid']
        bankname = request.form['bankname']
        stuffname = request.form['stuffname']
        address = request.form['address']
        phone = request.form['phone']
        datestartworking = request.form['datestartworking']

        return render_template("success.html", action="修改", succ=1, showurl=url_for("bank.stuff", page=0), messege=None)
    return render_template("edit.html", type=1)


@bp.route("/delstuff<string:pk>", methods=('GET', 'POST'))
def delstuff(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.stuff", page=0), messege=None)


@bp.route("/addbank", methods=('GET', 'POST'))
def addbank():
    if request.method == 'POST':
        bankname = request.form['bankname']
        bankcity = request.form['bankcity']
        property = request.form['property']
        print([bankname, bankcity, property])
        return render_template("success.html", action="添加", succ=1, showurl=url_for("bank.bank", page=0),
                               messege=None)
    return render_template("add.html", type=2)


@bp.route("/editbank<string:pk>", methods=('GET', 'POST'))
def editbank(pk):
    if request.method == 'POST':
        bankcity = request.form['bankcity']
        property = request.form['property']
        print([pk, bankcity, property])
        return render_template("success.html", action="修改", succ=1, showurl=url_for("bank.bank", page=0), messege=None)
    return render_template("edit.html", type=2)


@bp.route("/delbank<string:pk>", methods=('GET', 'POST'))
def delbank(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.bank", page=0), messege=None)


@bp.route("/success<string:p>", methods=('GET', 'POST'))
def success(p):
    return render_template("success.html", action="保存", succ=1, showurl=url_for("bank."+p, page=0), messege=None)


@bp.route("/", methods=("GET", "POST"))
def index(page=None):
    return redirect(url_for("bank.bank", page=0))
    # return render_template("login.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    return render_template("login.html")


