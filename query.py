import sqlalchemy as db
from sqlalchemy import Column, CHAR, FLOAT, DATE, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from BankManager.db import BankClass, StaffClass
# ClientClass, AccountClass, PersonInChargeClass, OpenAccountClass, OwningClass, LoanClass, PayLoanClass, \
# SaveAccountClass, CheckAccountClass



def getBank(session, name='', city='', propertylow=0, propertyhigh=1000000000, smallfirst=True, orderby='BankName'):
    bankList=[]
    for bank in session.query(BankClass) \
            .filter(BankClass.BankName.like('%'+name+'%'), BankClass.City.like('%'+city+'%'), BankClass.Property > propertylow, BankClass.Property < propertyhigh)\
            .order_by(BankClass.__getattribute__(BankClass, orderby)):
        # .order_by((1 if smallfirst else -1)*BankClass.__getattribute__(BankClass, orderby)):
        bankList.append([bank.BankName, bank.City, bank.Property])
    return bankList


def newBank(session, name, city, property):
    if(len(session.query(BankClass).filter(BankClass.BankName == name).all()) == 0):
        bank = BankClass(BankName=name, City=city, Property=property)
        session.add(bank)
    else:
        raise Exception("Bank Name Exists!")


def setBank(session, name, new, attribute):
    bank = session.query(BankClass).filter(BankClass.BankName == name).first()
    if(attribute == 'BankName'):
        if(len(session.query(BankClass).filter(BankClass.__getattribute__(BankClass, attribute) == new).all()) == 0):
            bank.__setattr__(attribute, new)
        else:
            raise Exception("Bank Name Exists!")
    else:
        bank.__setattr__(attribute, new)


#待完成：考虑约束的删除
def delBank(session, name):
    bank = session.query(BankClass).filter(BankClass.BankName == name).first()
    if(len(bank.StaffofBank) == 0
            and len(bank.AccountofBank) == 0
            and len(bank.LoanofBank) == 0):
        session.delete(session.query(BankClass).filter(BankClass.BankName == name).first())
    else:
        raise Exception("ForeignKey constraint.")


#date yyyy-mm-dd
def getStaff(session, id='', bank='', name='', phone='', address='',startdate='0000-01-01', enddate='9999-12-31' ,smallfirst=True, orderby='StaffID'):
    staffList=[]
    '''员工ID，所在支行，员工姓名，手机，住址，开始工作日期'''
    for staff in session.query(StaffClass) \
            .filter(StaffClass.StaffID.like('%'+id+'%'),
                    StaffClass.BankName.like('%'+bank+'%'),
                    StaffClass.StaffName.like('%'+name+'%'),
                    StaffClass.Phone.like('%'+phone+'%'),
                    StaffClass.Address.like('%'+address+'%'),
                    StaffClass.DateStartWorking > startdate,
                    StaffClass.DateStartWorking < enddate)\
            .order_by(StaffClass.__getattribute__(StaffClass, orderby)):
            #.order_by((1 if smallfirst else -1)*StaffClass.__getattribute__(StaffClass, orderby)):
        staffList.append([staff.StaffID, staff.BankName, staff.StaffName, staff.Phone, staff.Address, staff.DateStartWorking])
    return staffList


def newStaff(session, id, bank, name, phone, address, date):
    if(len(session.query(StaffClass).filter(StaffClass.StaffID == id).all()) == 0
            and len(session.query(BankClass).filter(BankClass.BankName == bank).all()) != 0):
        staff = StaffClass(StaffID=id, BankName=bank, StaffName=name, Phone=phone, Address=address, DateStartWorking=date)
        session.add(staff)
    else:
        raise Exception("Staff Id Exists or Bank Name not found")


def setStaff(session, id, new, attribute):
    staff = session.query(StaffClass).filter(StaffClass.StaffID == id).first()
    if(attribute == 'StaffID'):
        if (len(session.query(StaffClass).filter(
                StaffClass.__getattribute__(StaffClass, attribute) == new).all()) == 0):
            staff.__setattr__(attribute, new)
        else:
            raise Exception("Staff Name Exists!")
    else:
        staff.__setattr__(attribute, new)


def delStaff(session, id):
    if (len(session.query(StaffClass).filter(StaffClass.StaffID == id).first().ChargeofStaff) == 0):
        session.delete(session.query(StaffClass).filter(StaffClass.StaffID == id).first())
    else:
        raise Exception("ForeignKey constraint.")


def getClient(session, id='', name='', phone='', address= '', smallfirst=True, orderby='ClientID'):
    clientList=[]
    for client in session.query(ClientClass)\
            .filter(ClientClass.ClientID.like('%'+id+'%'),
                    ClientClass.ClientName.like('%'+name+'%'),
                    ClientClass.Phone.like('%'+phone+'%'),
                    ClientClass.Address.like('%'+address+'%'))\
            .order_by((1 if smallfirst else -1)*ClientClass.__getattribute__(ClientClass, orderby)):
        linkname=''
        for i in client.LinkofClient:
            linkname=linkname+i.LinkName
        clientList.append([client.ClientID, client.ClientName, client.Phone, client.Address, linkname])
    return clientList


def newClient(session, id, name, phone, address):
    if (len(session.query(ClientClass).filter(ClientClass.ClientID == id).all()) == 0):
        client = ClientClass(ClientID=id, ClientName=name, Phone=phone, Address=address)
        session.add(client)
    else:
        raise Exception("Staff Id Exists or Bank Name not found")


#def addLink(session):


def setClient(session, id, new, attribute):
    client = session.query(ClientClass).filter(ClientClass.ClientID == id).first()
    if (attribute == 'ClientID'):
        if (len(session.query(ClientClass).filter(
                ClientClass.__getattribute__(ClientClass, attribute) == new).all()) == 0):
            client.__setattr__(attribute, new)
        else:
            raise Exception("Staff Name Exists!")
    else:
        client.__setattr__(attribute, new)


def delClient(session):
    client = session.query(ClientClass).filter(ClientClass.ClientID == id).first()
    if (len(client.LinkofClient) == 0 ):
        session.delete(session.query(ClientClass).filter(ClientClass.ClientID == id).first())
    else:
        raise Exception("ForeignKey constraint.")


def getAccount(session, clientid='', clientname='', type='All', bank=''):
    checkaccountList=[]
    saveaccountList=[]
    namelist = session.query(ClientClass.ClientID).filter(ClientClass.ClientName.like('%'+clientname+'%')).all()
    for account in session.query(OpenAccountClass)\
            .filter(OpenAccountClass.ClientID.like('%'+clientid+'%'), OpenAccountClass.ClientID.in_(namelist), OpenAccountClass.BankName.like('%'+bank+'%'))\
            .order_by(OpenAccountClass.ClientID):
        if type != 'SaveAccount' and account.CheckAccountID != db.null :
            checkaccount = account.checkaccountid
            '''账户ID，账户所在银行，账户持有人ID，账户余额，账户开设时间，账户透支额'''
            checkaccountList.append([checkaccount.AccountID, checkaccount.BankName, checkaccount.ClientID,
                                checkaccount.Balance, checkaccount.DateOpening, checkaccount.Overdraft])
        if type != 'CheckAccount' and account.SaveAccountID != db.null :
            saveaccount = account.saveaccountid
            '''账户ID，账户类型，账户所在银行，账户持有人ID，账户余额，账户开设时间，汇率，货币类型'''
            saveaccountList.append([saveaccount.AccountID, saveaccount.BankName, saveaccount.ClientID,
                                saveaccount.Balance, saveaccount.DateOpening, saveaccount.Rate, saveaccount.MoneyType])
    return checkaccountList, saveaccountList


def addSaveAccount(session, accountid, clientid, bank, balance, date, rate, moneytype):
    if (len(session.query(AccountClass).filter(AccountClass.AccountID == accountid).all()) == 0):
        account = AccountClass(AcountID = accountid, Balance = balance, DateOpening = date)
        session.add(account)
    else:
        raise Exception("Account Id Exists")
    openaccount = session.query(OpenAccountClass).filter(OpenAccountClass.BankName == bank,
                                                         OpenAccountClass.ClientID == clientid).first()
    if (len(openaccount) == 0):
        openaccount = OpenAccountClass(BankName=bank, ClientID=clientid)
        session.add(openaccount)
    if(len(session.query(SaveAccountClass).filter(SaveAccountClass.AccountID == accountid).all()) == 0):
        account = SaveAccountClass(AcountID=accountid, BankName=bank, ClientID=clientid,
                               Balance=balance, DateOpening=date, Rate=rate, MoneyType=moneytype)
        session.add(account)
    else:
        raise Exception("Account Id Exists")
    openaccount.SaveAccountID = clientid


def addCheckAccount(session, accountid, clientid, bank, balance, date, overdraft):
    if (len(session.query(AccountClass).filter(AccountClass.AccountID == accountid).all()) == 0):
        account = AccountClass(AcountID=accountid, Balance=balance, DateOpening=date)
        session.add(account)
    else:
        raise Exception("Account Id Exists")
    openaccount=session.query(OpenAccountClass).filter(OpenAccountClass.BankName == bank,
                                           OpenAccountClass.ClientID == clientid).first()
    if(len(openaccount) == 0):
        openaccount = OpenAccountClass(BankName=bank, ClientID=clientid)
        session.add(openaccount)
    if (len(session.query(CheckAccountClass).filter(CheckAccountClass.AccountID == accountid).all()) == 0):
        account = CheckAccountClass(AcountID=accountid, BankName=bank, ClientID=clientid,
                               Balance=balance, DateOpening=date, Overdraft=overdraft)
        session.add(account)
    else:
        raise Exception("Account Id Exists")
    openaccount.CheckAccountID = clientid



def setAccount(session, accountid, new, attribute):
    account = session.query(AccountClass).filter(AccountClass.AccountID == accountid).first()
    if(attribute in ['Balance','DateOpening']):
        account.__setattr__(attribute, new)
    if (len(account.CheckofAccount) != 0):
        checkaccount = session.query(CheckAccountClass).filter(CheckAccountClass.AccountID == accountid).first()
        checkaccount.__setattr__(attribute, new)
    if (len(account.SaveofAccount) != 0):
        saveaccount = session.query(SaveAccountClass).filter(SaveAccountClass.AccountID == accountid).first()
        saveaccount.__setattr__(attribute, new)


def delAccount(session, accountid):
    account = session.query(AccountClass).filter(AccountClass.AccountID == accountid).first()
    if (len(account.SaveofAccount) != 0):
        session.delete(account.SaveofAccount[0].OpenofSave)
        session.delete(account.SaveofAccount[0])
    if (len(account.CheckofAccount) != 0):
        session.delete(account.CheckofAccount[0].OpenofSCheck)
        session.delete(account.CheckofAccount[0])
    session.delete(account)


def getLoan(session, clientid='', clientname='', bank=''):
    loanList=[]
    namelist = session.query(ClientClass.ClientID).filter(ClientClass.ClientName.like('%' + clientname + '%')).all()
    for loan in session.query(OwningClass,LoanClass) \
            .filter(OwningClass.ClientID.like('%' + clientid + '%'),
                    OwningClass.ClientID.in_(namelist),
                    OwningClass.loanid.BankName.like('%' + bank + '%')) \
            .order_by(OwningClass.ClientID):
        sum = 0
        state = '未发放'
        for pay in loan.PayofLoan:
            sum = sum + pay.Amount
        if(sum == loan.loanid.Amount):
            state = '已全部发放'
        elif (sum > 0):
            state = '发放中'
        loanList.append([loan.LoanID, loan.ClientID, loan.loanid.BankName, loan.loanid.Amount, state])
    return loanList


def getPay(session, loanid):
    payList = []
    for pay in session.query(PayLoanClass)\
            .filter(PayLoanClass.LoanID.like('%'+loanid+'%'))\
            .order_by(PayLoanClass.Date):
        payList.append([pay.PayID, pay.Date, pay.Amount])
    return payList


def addLoan(session, loanid, clientidlist, bank, amount):
    loan = LoanClass(LoanID=loanid, BankName=bank, Amount=amount)
    session.add(loan)
    for owner in clientidlist:
        own = OwningClass(ClientID=owner, LoanID=loanid)
        session.add(own)


def delLoan(session, loanid):
    loan = session.query(LoanClass).filter(LoanClass.LoanID == loanid).first()
    sum = 0
    for pay in loan.PayofLoan:
        sum = sum + pay.Amount
    if (sum < loan.loanid.Amount):
        raise Exception("未发放完成")
    else:
        session.delete(loan.OwnodLoan)
        session.delete(loan.PayofLoan)
        session.delete(loan)


def addPay(session, payid, loanid, date, amount):
    pay = PayLoanClass(PayID=payid, LoanID=loanid, Date=date, Amount=amount)
    session.add(pay)


#def calculate(session):


if __name__ == '__main__':
    #bank类的接口示例
    engine = db.create_engine('mysql+mysqlconnector://root:2161815@localhost:3306/test')
    DBSession = sessionmaker(bind=engine)
    Session = DBSession()
    delStaff(Session, '1145141919')
    try:
        newStaff(Session, '114514', '下北泽支行', '李田所', '1145141919810', '下北泽', '1919-08-10')
    except Exception as e:
        print(e)
    try:
        newStaff(Session, '19580101', '合肥支行', 'cwk', '191919191919', '伯克利', '1999-09-09')
    except Exception as e:
        print(e)
    Session.commit()
    #获取按资产顺序排序的银行列表
    print(getStaff(Session))
    #银行资产修改
    setStaff(Session,'114514', '1145141919', 'StaffID')
    Session.commit()
    #获取列表函数可选参数name、city、propertylow（下界）和propertyhigh（上界）
    print(getStaff(Session, orderby='DateStartWorking'))
    #根据name（primary key）删除支行
    delStaff(Session, '19580101')
    Session.commit()
    print(getStaff(Session))
    
