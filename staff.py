from flask import Blueprint
from flask import request
from flask import render_template
from flask import url_for

from BankManager.auth import login_required
from BankManager.db import session_scope
from BankManager.query import getStaff, newStaff, setStaff, delStaff

with session_scope() as session:
    global cont
    cont = getStaff(session)

bp = Blueprint("staff", __name__)

@bp.route("/staff<int:page>", methods=('GET', 'POST'))
def staff(page=None):
    if not page:
        page = 0
    if request.method == 'POST':
        staffid = request.form['staffid']
        bankname = request.form['bankname']
        staffname = request.form['staffname']
        phone = request.form['phone']
        minp = request.form['mindate']
        if not minp:
            minp = '0000-01-01'
        maxp = request.form['maxdate']
        if not maxp:
            maxp = '9999-12-31'
        waytosort = request.form['way']
        if waytosort == 'option0':
            global cont
            cont = []
        if waytosort == 'option1':
            with session_scope() as session:
                cont = getStaff(session, id=staffid, bank=bankname, \
                                name=staffname, phone=phone, startdate=minp, \
                                enddate=maxp, orderby='StaffID')
        if waytosort == 'option2':
            with session_scope() as session:
                cont = getStaff(session, id=staffid, bank=bankname, \
                                name=staffname, phone=phone, startdate=minp, \
                                enddate=maxp, orderby='StaffName')
        if waytosort == 'option3':
            with session_scope() as session:
                cont = getStaff(session, id=staffid, bank=bankname,\
                    name=staffname, phone=phone, startdate=minp,\
                    enddate=maxp, orderby='BankName')

    return render_template("staff-table.html", page=page, cont=cont, tot=len(cont))


@bp.route("/addstaff", methods=('GET', 'POST'))
def addstaff():
    if request.method == 'POST':
        error = None

        staffid = request.form['staffid']

        if not staffid:
            error = "Staff ID is required."

        bankname = request.form['bankname']

        if not bankname:
            error = "Bank Name is required."

        staffname = request.form['staffname']

        if not staffname:
            error = "Staff Name is required."

        address = request.form['address']

        if not address:
            error = "Staff Address is required."

        phone = request.form['phone']

        if not phone:
            error = "Staff Phone Number is required."

        datestartworking = request.form['datestartworking']

        if not datestartworking:
            error = "Date Start Working is required."

        if error is not None:
            print(error)
            flash(error)
        else:
            with session_scope() as session:
                newStaff(session, staffid, bankname, staffname, phone, address, datestartworking)
            with session_scope() as session:
                global cont
                cont = getStaff(session)

        return render_template("success.html", action="添加", succ=1, showurl=url_for("staff.staff", page=0),
                               messege=None)
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

        with session_scope() as session:
            if staffid:
                setStaff(session, pk, staffid, "StaffID")
            if bankname:
                setStaff(session, pk, bankname, "BankName")
            if staffname:
                setStaff(session, pk, staffname, "StaffName")
            if address:
                setStaff(session, pk, address, "Address")
            if phone:
                setStaff(session, pk, phone, "Phone")
            if datestartworking:
                setStaff(session, pk, datestartworking, "DateStartWorking")

        with session_scope() as session:
            global cont
            cont = getStaff(session)
        return render_template("success.html", action="修改", succ=1, showurl=url_for("staff.staff", page=0), messege=None)
    return render_template("edit.html", type=1)


@bp.route("/delstaff<string:pk>", methods=('GET', 'POST'))
def delstaff(pk):
    with session_scope() as session:
        delStaff(session, pk)
    with session_scope() as session:
        global cont
        cont = getStaff(session)
    return render_template("success.html", action="删除", succ=1, showurl=url_for("staff.staff", page=0), messege=None)
