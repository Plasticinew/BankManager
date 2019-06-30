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
    return render_template("edit.html", type=4)


@bp.route("/editcheckaccount<string:pk>", methods=('GET', 'POST'))
def editcheckaccount(pk):
    if request.method == 'POST':
        accountid = request.form['accountid']
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
