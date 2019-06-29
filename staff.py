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

        return render_template("success.html", action="修改", succ=1, showurl=url_for("bank.staff", page=0), messege=None)
    return render_template("edit.html", type=1)


@bp.route("/delstaff<string:pk>", methods=('GET', 'POST'))
def delstaff(pk):
    return render_template("success.html", action="删除", succ=1, showurl=url_for("bank.staff", page=0), messege=None)
