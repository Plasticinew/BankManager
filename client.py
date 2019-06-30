from flask import Blueprint
from flask import render_template
from flask import request
from flask import url_for

from BankManager.auth import login_required
from BankManager.db import session_scope
from BankManager.query import getClient, newClient, setClient, delClient
from BankManager.error import flash

with session_scope() as session:
    global cont
    cont = getClient(session)

bp = Blueprint("client", __name__)

@bp.route("/client<int:page>", methods=('GET', 'POST'))
@login_required
def client(page=None):
    if not page:
        page = 0
    if request.method == 'POST':
        global cont
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        linkid = request.form['linkid']
        linkname = request.form['linkname']
        phone = request.form['phone']
        waytosort = request.form['way']
        if waytosort == 'option0':
            cont = []
        if waytosort == 'option1':
            with session_scope() as session:
                cont = getClient(session, id=clientid, name=clientname,\
                                 phone=phone, orderby="ClientID")
        if waytosort == 'option2':
            with session_scope() as session:
                cont = getClient(session, id=clientid, name=clientname,\
                                 phone=phone, orderby="ClientName")
        if waytosort == 'option3':
            cont = []
            #todo:linkid
        if waytosort == 'option4':
            cont = []
            #todo:linkname

    return render_template("client-table.html", page=page, cont=cont, tot=len(cont))

@bp.route("/addclient", methods=('GET', 'POST'))
@login_required
def addclient():
    if request.method == 'POST':

        error = None

        clientid = request.form['clientid']

        if not clientid:
            error = "ClientID is required."

        clientname = request.form['clientname']

        if not clientname:
            error = "Client Name is required."

        # linkid = request.form['linkid']
        #
        # if not linkid:
        #     error = "Linkman ID is required."
        #
        # linkname = request.form['linkname']

        address = request.form['address']

        if not address:
            error = "Address is required."

        phone = request.form['phone']

        if not phone:
            error = "Phone Number is required."

        if error is not None:
            print(error)
            return flash(error, "增加客户", url_for("client.client", page=0))
        else:
            with session_scope() as session:
                newClient(session, clientid, clientname, phone, address)

            with session_scope() as session:
                global cont
                cont = getClient(session)

            return render_template("success.html", action="添加", succ=1, showurl=url_for("client.client", page=0),
                               messege=None)

    return render_template("edit.html", type=3)

@bp.route("/editclient<string:pk>", methods=('GET', 'POST'))
@login_required
def editclient(pk):
    if request.method == 'POST':
        clientid = request.form['clientid']
        clientname = request.form['clientname']
        # staffid = request.form['staffid']
        # staffname = request.form['staffname']
        address = request.form['address']
        phone = request.form['phone']
        with session_scope() as session:
            if clientid:
                try:
                    setClient(session, pk, clientid, "ClientID")
                except Exception as e:
                    return flash(e.args[0], "修改客户信息", url_for("client.client", page=0))

            if clientname:
                setClient(session, pk, clientname, "ClientName")

            if phone:
                setClient(session, pk, phone, "Phone")

            if address:
                setClient(session, pk, address, "Address")

        with session_scope() as session:
            global cont
            cont = getClient(session)

        return render_template("success.html", action="修改", succ=1, showurl=url_for("client.client", page=0), messege=None)
    return render_template("edit.html", type=3)


@bp.route("/delclient<string:pk>", methods=('GET', 'POST'))
@login_required
def delclient(pk):
    with session_scope() as session:
        try:
            delClient(session, pk)
        except Exception as e:
            return flash(e.args[0], "删除客户信息", url_for("client.client", page=0))
    with session_scope() as session:
        global cont
        cont = getClient(session)
    return render_template("success.html", action="删除", succ=1, showurl=url_for("client.client", page=0), messege=None)