import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from BankManager.db import BankClass, StaffClass


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


class Staff:
    def __init__(self, session):
        self.session = session

    '''
    date yyyy-mm-dd
    '''
    def getStaff(self, id='', bank='', name='', phone='', address='',startdate='', enddate='' ,smallfirst=True, orderby='StaffID'):
        staffList=[]
        for staff in self.session.query(StaffClass) \
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

    def newStaff(self, name, city, property):
        if(len(self.session.query(BankClass).filter(BankClass.BankName == name).all()) == 0):
            bank = BankClass(BankName=name, City=city, Property=property)
            self.session.add(bank)
        else:
            raise Exception("Bank Name Exists!")

    def setStaff(self, attribute, id, new):
        staff = self.session.query(StaffClass).filter(StaffClass.StaffID == id).first()
        if(attribute == 'StaffID'):
            if (len(self.session.query(StaffClass).filter(
                    StaffClass.__getattribute__(StaffClass, attribute) == new).all()) == 0):
                staff.__setattr__(attribute, new)
            else:
                raise Exception("Bank Name Exists!")
        else:
            staff.__setattr__(attribute, new)



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
    
