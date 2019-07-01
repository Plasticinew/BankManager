import sqlalchemy as db
import matplotlib.pyplot as plt
from pandas import date_range
from pandas import to_datetime
import datetime
from sqlalchemy import Column, CHAR, FLOAT, DATE, ForeignKey, null
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from BankManager.db import BankClass, StaffClass, LogClass,\
 ClientClass, AccountClass, PersonInChargeClass, OpenAccountClass, OwningClass, LoanClass, PayLoanClass, \
 SaveAccountClass, CheckAccountClass





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
def getStaff(session, id='', bank='', name='', phone='', address='',startdate='0000-01-01', enddate='9999-12-31', smallfirst=True, orderby='StaffID'):
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


def getClient(session, id='', name='', phone='', address= '', orderby='ClientID'):
    clientList=[]
    for client in session.query(ClientClass)\
            .filter(ClientClass.ClientID.like('%'+id+'%'),
                    ClientClass.ClientName.like('%'+name+'%'),
                    ClientClass.Phone.like('%'+phone+'%'),
                    ClientClass.Address.like('%'+address+'%')) \
            .order_by(ClientClass.__getattribute__(ClientClass, orderby)):
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


def getCheckAccount(session, accountid='', clientid='', clientname='', bank='', orderby='CheckAccountID'):
    checkaccountList=[]
    for account, client in session.query(OpenAccountClass, ClientClass)\
            .filter(OpenAccountClass.ClientID.like('%'+clientid+'%'),
                    OpenAccountClass.ClientID == ClientClass.ClientID,
                    OpenAccountClass.CheckAccountID.like('%'+accountid+'%'),
                    OpenAccountClass.BankName.like('%'+bank+'%'),
                    ClientClass.ClientName.like('%' + clientname + '%'))\
            .order_by(OpenAccountClass.__getattribute__(OpenAccountClass, orderby)):
        checkaccount = account.checkaccountid
        '''账户ID，账户所在银行，账户持有人ID，账户余额，账户开设时间，账户透支额'''
        checkaccountList.append([checkaccount.AccountID, account.BankName, account.ClientID, account.clientid.ClientName,
                          checkaccount.Balance, checkaccount.DateOpening, checkaccount.Overdraft])
    return checkaccountList


def getSaveAccount(session, accountid='', clientid='', clientname='', bank='', orderby='SaveAccountID'):
    saveaccountList=[]
    # namelist = session.query(ClientClass.ClientID).filter(ClientClass.ClientName.like('%'+clientname+'%')).all()
    for account, client in session.query(OpenAccountClass, ClientClass)\
            .filter(OpenAccountClass.ClientID.like('%'+clientid+'%'),
                    OpenAccountClass.ClientID == ClientClass.ClientID,
                    OpenAccountClass.SaveAccountID.like('%' + accountid + '%'),
                    OpenAccountClass.BankName.like('%'+bank+'%'),
                    ClientClass.ClientName.like('%' + clientname + '%'))\
            .order_by(OpenAccountClass.__getattribute__(OpenAccountClass, orderby)):
        saveaccount = account.saveaccountid
        '''账户ID，账户类型，账户所在银行，账户持有人ID，账户余额，账户开设时间，汇率，货币类型'''
        saveaccountList.append([saveaccount.AccountID, account.BankName, account.ClientID, account.clientid.ClientName,
                          saveaccount.Balance, saveaccount.DateOpening, saveaccount.Rate, saveaccount.MoneyType])
    return saveaccountList


def newSaveAccount(session, accountid, clientid, bank, balance, date, rate, moneytype):
    if (len(session.query(AccountClass).filter(AccountClass.AccountID == accountid).all()) == 0):
        account = AccountClass(AccountID = accountid, Balance = balance, DateOpening = date)
        session.add(account)
    else:
        raise Exception("Account Id Exists")
    if (len(session.query(SaveAccountClass).filter(SaveAccountClass.AccountID == accountid).all()) == 0):
        account = SaveAccountClass(AccountID=accountid,
                                   Balance=balance, DateOpening=date, Rate=rate, MoneyType=moneytype)
        session.add(account)
    else:
        raise Exception("Account Id Exists")
    session.commit()
    openaccount = session.query(OpenAccountClass).filter(OpenAccountClass.BankName == bank,
                                                         OpenAccountClass.ClientID == clientid).all()
    if (len(openaccount) == 0):
        openaccount = OpenAccountClass(BankName=bank, ClientID=clientid, SaveAccountID=accountid)
        session.add(openaccount)
    else:
        openaccount[0].SaveAccountID = accountid
    log = LogClass(Time=date, AccountID=accountid, Action=balance, newValue=balance,Bank=bank,
                   Type='SaveAccount')
    session.add(log)


def newCheckAccount(session, accountid, clientid, bank, balance, date, overdraft):
    if (len(session.query(AccountClass).filter(AccountClass.AccountID == accountid).all()) == 0):
        account = AccountClass(AccountID=accountid, Balance=balance, DateOpening=date)
        session.add(account)
    else:
        raise Exception("Account Id Exists")
    if (len(session.query(CheckAccountClass).filter(CheckAccountClass.AccountID == accountid).all()) == 0):
        account = CheckAccountClass(AccountID=accountid, Balance=balance, DateOpening=date, Overdraft=overdraft)
        session.add(account)
    else:
        raise Exception("Account Id Exists")
    session.commit()
    openaccount=session.query(OpenAccountClass).filter(OpenAccountClass.BankName == bank,
                                           OpenAccountClass.ClientID == clientid).all()
    if(len(openaccount) == 0):
        openaccount = OpenAccountClass(BankName=bank, ClientID=clientid, CheckAccountID=accountid, SaveAccountID=None)
        session.add(openaccount)
    else:
        openaccount[0].CheckAccountID = accountid
    log = LogClass(Time=date, AccountID=accountid, Action=balance, newValue=balance, Bank=bank,
                   Type='CheckAccount')
    session.add(log)


def setAccount_balance(session, accountid, balance, date):
    account = session.query(AccountClass).filter(AccountClass.AccountID == accountid).first()
    oldbalance = account.Balance
    account.Balance = balance
    account.DateOpening = date
    if (len(account.CheckofAccount) != 0):
        checkaccount = session.query(CheckAccountClass).filter(CheckAccountClass.AccountID == accountid).first()
        checkaccount.Balance = balance
        checkaccount.DateOpening = date
        log = LogClass(Time=date, AccountID=accountid, Action=balance - oldbalance, newValue=balance,
                       Type='CheckAccount', Bank=checkaccount.OpenofCheck[0].BankName)
        session.add(log)
    if (len(account.SaveofAccount) != 0):
        saveaccount = session.query(SaveAccountClass).filter(SaveAccountClass.AccountID == accountid).first()
        saveaccount.Balance = balance
        saveaccount.DateOpening = date
        log = LogClass(Time=date, AccountID=accountid, Action=balance - oldbalance, newValue=balance,
                       Type='SaveAccount', Bank=saveaccount.OpenofCheck[0].BankName)
        session.add(log)


def setAccount_others(session, accountid, new, attribute):
    account = session.query(AccountClass).filter(AccountClass.AccountID == accountid).first()
    if (len(account.CheckofAccount) != 0):
        if (attribute == 'BankName' or attribute == 'ClientID'):
            account.CheckofAccount[0].OpenofCheck[0].__setattr__(attribute, new)
        else:
            checkaccount = session.query(CheckAccountClass).filter(CheckAccountClass.AccountID == accountid).first()
            checkaccount.__setattr__(attribute, new)
    if (len(account.SaveofAccount) != 0):
        if (attribute == 'BankName' or attribute == 'ClientID'):
            account.SaveofAccount[0].OpenofSave[0].__setattr__(attribute, new)
        else:
            saveaccount = session.query(SaveAccountClass).filter(SaveAccountClass.AccountID == accountid).first()
            saveaccount.__setattr__(attribute, new)


def delAccount(session, accountid):
    account = session.query(AccountClass).filter(AccountClass.AccountID == accountid).first()
    if (len(account.SaveofAccount) != 0):
        log = LogClass(Time=account.SaveofAccount[0].DateOpening, AccountID=account.SaveofAccount[0].AccountID,
                       Action=-account.SaveofAccount[0].Balance, newValue=0,
                       Type='SaveAccount', Bank=account.SaveofAccount[0].OpenofSave[0].BankName)
        session.add(log)
        pk = (account.SaveofAccount[0].OpenofSave[0].BankName, \
              account.SaveofAccount[0].OpenofSave[0].ClientID)
        session.delete(account.SaveofAccount[0])
        session.commit()
        # session.delete(account.SaveofAccount[0].OpenofSave[0])
    if (len(account.CheckofAccount) != 0):
        log = LogClass(Time=account.CheckofAccount[0].DateOpening, AccountID=account.CheckofAccount[0].AccountID,
                       Action=-account.CheckofAccount[0].Balance, newValue=0,
                       Type='CheckAccount', Bank=account.CheckofAccount[0].OpenofCheck[0].BankName)
        session.add(log)
        pk = (account.CheckofAccount[0].OpenofCheck[0].BankName, \
              account.CheckofAccount[0].OpenofCheck[0].ClientID)
        session.delete(account.CheckofAccount[0])
        session.commit()
        # session.delete(account.CheckofAccount[0].OpenofCheck[0])

    for openaccount in session.query(OpenAccountClass)\
            .filter(OpenAccountClass.BankName == pk[0] and OpenAccountClass.ClientID == pk[1]):
        if openaccount.SaveAccountID is None and openaccount.CheckAccountID is None:

            session.delete(openaccount)

    session.delete(account)



def getLoan(session, loanid='', clientid='', clientname='', bank=''):
    loanList=[]
    # namelist = session.query(ClientClass.ClientID).filter(ClientClass.ClientName.like('%' + clientname + '%')).all()
    for loan, own, client in session.query(LoanClass,OwningClass,ClientClass)\
            .filter(OwningClass.ClientID.like('%' + clientid + '%'),
                    LoanClass.LoanID.like('%'+loanid+'%'),
                    ClientClass.ClientID == OwningClass.ClientID,
                    LoanClass.LoanID == OwningClass.LoanID,
                    ClientClass.ClientID.like('%'+clientname+'%'),
                    LoanClass.BankName.like('%' + bank + '%')) \
            .order_by(OwningClass.ClientID):
        sum = 0
        state = '未发放'
        for pay in loan.PayofLoan:
            sum = sum + pay.Amount
        if(sum == loan.Amount):
            state = '已全部发放'
        elif (sum > 0):
            state = '发放中'
        loanList.append([loan.LoanID, own.ClientID, client.ClientName, loan.BankName, loan.Amount, state])
    return loanList

def getPay(session, loanid):
    payList = []
    for pay in session.query(PayLoanClass)\
            .filter(PayLoanClass.LoanID.like('%' + str(loanid) + '%'))\
            .order_by(PayLoanClass.Date):
        payList.append([pay.PayID, pay.Date, pay.Amount])
    return payList


def newLoan(session, loanid, clientidlist, bank, amount):
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


def calculate(session):
    bank=[]
    usercount=[]
    checkwealth=[]
    savewealth=[]
    for bankname in session.query(BankClass):
        bankname = bankname.BankName
        bank.append(bankname)
        usercount.append(len(session.query(OpenAccountClass).filter(OpenAccountClass.BankName==bankname).all()))
        value = 0
        for checkaccount, openaccount in session.query(CheckAccountClass, OpenAccountClass)\
                .filter(OpenAccountClass.CheckAccountID == CheckAccountClass.AccountID,
                        OpenAccountClass.BankName == bankname):
            value = value + checkaccount.Balance
        checkwealth.append(value)
        value = 0
        for saveaccount, openaccount in session.query(SaveAccountClass, OpenAccountClass) \
                .filter(OpenAccountClass.SaveAccountID == SaveAccountClass.AccountID,
                        OpenAccountClass.BankName == bankname):
            value = value + saveaccount.Balance
        savewealth.append(value)
    date = date_range('2015-01-01', datetime.date.today(), freq='MS')
    usercount_detail = []
    checkwealth_detail = []
    savewealth_detail = []
    for bankname in session.query(BankClass):
        bankname = bankname.BankName
        u_detail = []
        c_detail = []
        s_detail = []
        ucount = 0
        slice = date[1] - date[0]
        for month in date_range('2015-01-01', datetime.date.today(), freq='MS'):
            # slice = datetime.timedelta(days=30)
            c_sum = 0
            s_sum = 0

            for log in session.query(LogClass).filter(LogClass.Bank == bankname, LogClass.Time > month.to_pydatetime().date(),
                                                      LogClass.Time < (month + slice).to_pydatetime().date()).order_by(LogClass.Time):
                if(log.Action == log.newValue):
                    ucount=ucount+1
                if(log.Type == 'CheckAccount'):
                    c_sum = c_sum + log.Action
                if (log.Type == 'SaveAccount'):
                    s_sum = s_sum + log.Action
            u_detail.append(ucount)
            c_detail.append(c_sum)
            s_detail.append(s_sum)
        usercount_detail.append(u_detail)
        checkwealth_detail.append(c_detail)
        savewealth_detail.append(s_detail)
    '''银行列表，月份列表，
    按银行排序：用户总量列表，支票账户总价值列表，储蓄账户总价值列表，
    按银行排序并按月份排序：用户量详细列表，支票账户详细列表，储蓄账户详细列表'''
    # plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.pie(usercount, labels=bank)
    plt.title('User Proportion')
    plt.savefig('BankManager/static/usercount.png', format='png')
    plt.close()
    plt.pie(checkwealth, labels=bank)
    plt.title('Check Account Proportion')
    plt.savefig('BankManager/static/check.png', format='png')
    plt.close()
    plt.pie(savewealth, labels=bank)
    plt.title('Saving Account Proportion')
    plt.savefig('BankManager/static/save.png', format='png')
    plt.close()
    for i in range(len(bank)):
        plt.plot(date, usercount_detail[i], label=str(bank[i]))
    plt.xlabel('Month')
    plt.ylabel('User Count')
    plt.title('User Count Per Month')
    plt.legend(loc='upper left')
    plt.savefig('BankManager/static/user_detail.png', format='png')
    plt.close()
    for i in range(len(bank)):
        plt.plot(date, checkwealth_detail[i], label=str(bank[i]))
    plt.xlabel('Month')
    plt.ylabel('Check Account Total')
    plt.title('Check Account Total Per Month')
    plt.legend(loc='upper left')
    plt.savefig('BankManager/static/check_detail.png', format='png')
    plt.close()
    for i in range(len(bank)):
        plt.plot(date, savewealth_detail[i], label=str(bank[i]))
    plt.xlabel('Month')
    plt.ylabel('Saving Account Total')
    plt.title('Saving Account Total Per Month')
    plt.legend(loc='upper left')
    plt.savefig('BankManager/static/save_detail.png', format='png')
    plt.close()
    for i in range(len(bank)):
        new_user = []
        new_index = []
        count = 0
        user = 0
        index = 0
        for j in range(len(date)):
            user = usercount_detail[i][j]
            count = count + 1
            if count == 4:
                new_user.append(user)
                new_index.append(index)
                count = 0
                user = 0
                index = index + 1
        plt.plot(new_index, new_user, label=str(bank[i]))
    plt.xlabel('Season')
    plt.ylabel('User Count')
    plt.title('User Count Per Season')
    plt.legend(loc='upper left')
    plt.savefig('BankManager/static/user_detail_4.png', format='png')
    plt.close()
    for i in range(len(bank)):
        new_user = []
        new_index = []
        count = 0
        user = 0
        index = 0
        for j in range(len(date)):
            count = count + 1
            user = user + checkwealth_detail[i][j]
            if count == 4:
                new_user.append(user)
                new_index.append(index)
                count = 0
                user = 0
                index = index + 1
        plt.plot(new_index, new_user, label=str(bank[i]))
    plt.xlabel('Season')
    plt.ylabel('Check Account Total')
    plt.title('Check Account Total Per Season')
    plt.legend(loc='upper left')
    plt.savefig('BankManager/static/check_detail_4.png', format='png')
    plt.close()
    for i in range(len(bank)):
        new_user = []
        new_index = []
        count = 0
        user = 0
        index = 0
        for j in range(len(date)):
            user = user + savewealth_detail[i][j]
            count = count + 1
            if count == 4:
                new_user.append(user)
                new_index.append(index)
                count = 0
                user = 0
                index = index + 1
        plt.plot(new_index, new_user, label=str(bank[i]))
    plt.xlabel('Season')
    plt.ylabel('Saving Account Total')
    plt.title('Saving Account Total Per Season')
    plt.legend(loc='upper left')
    plt.savefig('BankManager/static/save_detail_4.png', format='png')
    plt.close()
    for i in range(len(bank)):
        new_user = []
        new_index = []
        count = 0
        user = 0
        index = 0
        for j in range(len(date)):
            user = usercount_detail[i][j]
            count = count + 1
            if count == 12:
                new_user.append(user)
                new_index.append(index)
                count = 0
                user = 0
                index = index + 1
        plt.plot(new_index, new_user, label=str(bank[i]))
    plt.xlabel('Year')
    plt.ylabel('User Count')
    plt.title('User Count Per Year')
    plt.legend(loc='upper left')
    plt.savefig('BankManager/static/user_detail_12.png', format='png')
    plt.close()
    for i in range(len(bank)):
        new_user = []
        new_index = []
        count = 0
        user = 0
        index = 0
        for j in range(len(date)):
            user = user + checkwealth_detail[i][j]
            count = count + 1
            if count == 12:
                new_user.append(user)
                new_index.append(index)
                count = 0
                user = 0
                index = index + 1
        plt.plot(new_index, new_user, label=str(bank[i]))
    plt.xlabel('Year')
    plt.ylabel('Check Account Total')
    plt.title('Check Account Total Per Year')
    plt.legend(loc='upper left')
    plt.savefig('BankManager/static/check_detail_12.png', format='png')
    plt.close()
    for i in range(len(bank)):
        new_user = []
        new_index = []
        count = 0
        user = 0
        index = 0
        for j in range(len(date)):
            user = user + savewealth_detail[i][j]
            count = count + 1
            if count == 12:
                new_user.append(user)
                new_index.append(index)
                count = 0
                user = 0
                index = index + 1
        plt.plot(new_index, new_user, label=str(bank[i]))
    plt.xlabel('Year')
    plt.ylabel('Saving Account Total')
    plt.title('Saving Account Total Per Year')
    plt.legend(loc='upper left')
    plt.savefig('BankManager/static/save_detail_12.png', format='png')
    plt.close()
    return bank, date, usercount, checkwealth, savewealth, usercount_detail, checkwealth_detail, savewealth_detail
