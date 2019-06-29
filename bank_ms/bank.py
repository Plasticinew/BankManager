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
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000'],
            ['aa', 'aaa', '100'],
            ['bb', 'bbb', '1000'],
            ['cc', 'ccc', '10000']]
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        waytosort = request.form['way']
        cont = [[name, city, waytosort]]

    return render_template("admin-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/addbank", methods=('GET', 'POST'))
def addbank():
    if request.method == 'POST':
        bankname = request.form['bankname']
        bankcity = request.form['bankcity']
        property = request.form['property']
        print([bankname, bankcity, property])
    return render_template("add.html", type=0)

@bp.route("/", methods=("GET", "POST"))
def index(page=None):
    return redirect(url_for("bank.bank", page=0))


