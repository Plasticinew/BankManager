from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort


bp = Blueprint("bank", __name__)


@bp.route("/", methods=('GET', 'POST'))
def index():
    page = 0
    cont = []
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

    return render_template("admin-table.html", page=page, cont=cont[page*10: min(page*10+10, len(cont))], tot=len(cont))


@bp.route("/table<int:page>", methods=("GET", "POST"))
def table(page):
    cont = []
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

    return render_template("admin-table.html", page=page, cont=cont[page*10: min(page*10+10, len(cont))], tot=len(cont))


