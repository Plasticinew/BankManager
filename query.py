import sqlalchemy as db
from sqlalchemy import Column, CHAR, FLOAT, DATE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BankClass(Base):
    __tablename__ = 'Bank'

    BankName = db.Column(db.CHAR(255), primary_key=True, nullable=False)
    City = db.Column(db.CHAR(255), nullable=False)
    Property = db.Column(db.INT, nullable=False)
    #Workers = db.orm.relationship('银行员工')


class StaffClass(Base):
    __tablename__ = 'Staff'

    StaffID = db.Column(db.CHAR(18), primary_key=True, nullable=False)
    BankName = db.Column(db.CHAR(255), db.ForeignKey('Bank.BankName'),nullable=False)
    StaffName = db.Column(db.CHAR(18), nullable=False)
    Phone = db.Column(db.CHAR(14), nullable=False)
    Address = db.Column(db.CHAR(255), nullable=False)
    DateStartWorking = db.Column(db.DATE, nullable=False)
    bankname = db.orm.relationship('BankClass',backref='StaffofBank')


class ClientClass(Base):
    __tablename__ = 'Client'

    ClientID = db.Column(db.CHAR(18), primary_key=True, nullable=False)
    LinkID = db.Column(db.CHAR(18))
    LinkName = db.Column(db.CHAR(16))
    ClientName = db.Column(db.CHAR(18), nullable=False)
    Phone = db.Column(db.CHAR(14), nullable=False)
    Address = db.Column(db.CHAR(255), nullable=False)


class AccountClass(Base):
    __tablename__ = 'Account'

    AccountID = Column(CHAR(11), nullable=True)
    Balance = Column(FLOAT, nullable=True)
    DateOpening = Column(DATE, nullable=True)





class PersonInChargeClass(Base):
    __tablename__ = 'PersonInCharge'

    ClientID = db.Column(db.CHAR(18), db.ForeignKey('Staff.StaffID'), primary_key=True, nullable=False)
    StaffID = db.Column(db.CHAR(18), db.ForeignKey('Staff.StaffID'), primary_key=True, nullable=False)




def getBank(session, name='', city='', propertylow=0, propertyhigh=1000000000, smallfirst=True, orderby='BankName'):
    bankList=[]
    for bank in session.query(BankClass) \
            .filter(BankClass.BankName.like('%'+name+'%'), BankClass.City.like('%'+city+'%'), BankClass.Property > propertylow, BankClass.Property < propertyhigh)\
            .order_by((1 if smallfirst else -1)*BankClass.__getattribute__(BankClass, orderby)):
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
    if(len(session.query(BankClass).filter(BankClass.BankName == name).first().StaffofBank) == 0):
        session.delete(session.query(BankClass).filter(BankClass.BankName == name).first())
    else:
        raise Exception("ForeignKey constraint.")


#date yyyy-mm-dd
def getStaff(session, id='', bank='', name='', phone='', address='',startdate='', enddate='' ,smallfirst=True, orderby='StaffID'):
    staffList=[]
    for staff in session.query(StaffClass) \
            .filter(StaffClass.StaffID.like('%'+id+'%'),
                    StaffClass.BankName.like('%'+bank+'%'),
                    StaffClass.StaffName.like('%'+name+'%'),
                    StaffClass.Phone.like('%'+phone+'%'),
                    StaffClass.Address.like('%'+address+'%'),
                    StaffClass.DateStartWorking > startdate,
                    StaffClass.DateStartWorking < enddate)\
            .order_by((1 if smallfirst else -1)*StaffClass.__getattribute__(StaffClass, orderby)):
        staffList.append([staff.StaffID, staff.BankName, staff.StaffName, staff.Phone, staff.Address, staff.DateStartWorking])
    return staffList


def newStaff(session, id, bank, name, phone, address, date):
    if(len(session.query(StaffClass).filter(StaffClass.StaffID == id).all()) == 0
            & len(session.query(StaffClass).filter(StaffClass.BankName == bank).all()) != 0):
        staff = StaffClass(id,bank,name,phone,address,date)
        session.add(staff)
    else:
        raise Exception("Staff Id Exists or Bank Name not found")


def setStaff(session, attribute, id, new):
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
    if (len(session.query(StaffClass).filter(StaffClass.StaffID == id).first().StaffofBank) == 0):
        session.delete(session.query(StaffClass).filter(StaffClass.StaffID == id).first())
    else:
        raise Exception("ForeignKey constraint.")

if __name__ == '__main__':
    #bank类的接口示例
    engine = db.create_engine('mysql+mysqlconnector://root:2161815@localhost:3306/test')
    DBSession = sessionmaker(bind=engine)
    Session = DBSession()
    #添加支行信息
    try:
        newBank(Session, '下北泽支行', '下北泽', 43962800)
        newBank(Session, '合肥支行', '合肥', 1919810)
    except Exception as e:
        print(e)
    newBank(Session, '济南支行', '济南', 114514)
    Session.commit()
    #获取按资产顺序排序的银行列表
    print(getBank(Session, orderby='Property'))
    #银行资产修改
    setBank(Session,'济南支行', 11400, 'Property')
    Session.commit()
    #获取列表函数可选参数name、city、propertylow（下界）和propertyhigh（上界）
    print(getBank(Session,city='济南',propertylow=1000,propertyhigh=1000000,orderby='City'))
    #根据name（primary key）删除支行
    delBank(Session, '济南支行')
    print(getBank(Session))
    
