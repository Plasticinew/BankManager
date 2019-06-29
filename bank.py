from flask import Blueprint
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template

from BankManager.db import get_dbSession
# from BankManager.db import BankQuery
from BankManager.db import Bank
from BankManager.auth import login_required



bp = Blueprint("bank", __name__)
page_length = 10

@bp.route("/", methods=('GET', 'POST'))
def index(page=None):
    return redirect(url_for("bank.bank", page=0))

@bp.route("/bank<int:page>", methods=('GET', 'POST'))
def bank(page=None):
    if not page:
        page = 0
    cont = getBankOrderByName()
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        waytosort = request.form['way']
        if waytosort == 'option2':
            cont = getBankOrderByName(name, city)

    return render_template("admin-table.html", page=page, cont=cont, tot=len(cont))

@bp.route("/addbank", methods=('GET', 'POST'))
def addbank():
    if request.method == 'POST':
        bankname = request.form['bankname']
        bankcity = request.form['bankcity']
        property = request.form['property']
        print([bankname, bankcity, property])
    return render_template("add.html", type=0)

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        bankname = request.form["BankName"]
        city = request.form["City"]
        property = request.form["Property"]
        error = None

        if not bankname:
            error = "Bank Name is required."

        if not city:
            error = "City is required."

        if not property:
            error = "Property is required."

        if error is not None:
            flash(error)
        else:
            DBSession = get_dbSession()
            DBSession.add(Bank(\
                BankName=bankname, City=city,\
                Property=property))
            DBSession.commit()
            return redirect(url_for("bank.index"))

def getBankOrderByName(name='', city='', ascending=True):
    session = get_dbSession()
    banklist = []
    for bank in session.query(Bank)\
        .filter(Bank.BankName.like('%' + name + '%'),\
                Bank.City.like('%' + city + '%')):
        # .order_by((1 if ascending else -1) * Bank.BankName):
        banklist.append((bank.BankName, bank.City, bank.Property))
    return banklist