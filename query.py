import sqlalchemy as db
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


class Bank:
    "支行管理的接口类，提供了三种排序方式的获取和筛选接口，以及增改删接口"
    def __init__(self, session):
        self.session = session

    def getBank(self, name='', city='', propertylow=0, propertyhigh=1000000000, smallfirst=True, orderby='BankName'):
        bankList=[]
        for bank in self.session.query(BankClass) \
                .filter(BankClass.BankName.like('%'+name+'%'), BankClass.City.like('%'+city+'%'), BankClass.Property > propertylow, BankClass.Property < propertyhigh)\
                .order_by((1 if smallfirst else -1)*BankClass.__getattribute__(BankClass, orderby)):
            bankList.append([bank.BankName, bank.City, bank.Property])
        return bankList

    def newBank(self, name, city, property):
        if(len(self.session.query(BankClass).filter(BankClass.BankName == name).all()) == 0):
            bank = BankClass(BankName=name, City=city, Property=property)
            self.session.add(bank)
        else:
            print("Bank Name Exists!")
        self.session.commit()

    def setBank(self, name, new, attribute):
        bank = self.session.query(BankClass).filter(BankClass.BankName == name).first()
        if(len(self.session.query(BankClass).filter(BankClass.__getattribute__(BankClass, attribute) == new).all()) == 0):
            bank.__setattr__(attribute, new)
        else:
            print("Bank Name Exists!")
        self.session.commit()

    #待完成：考虑约束的删除
    def delBank(self, name):
        if(len(self.session.query(BankClass).filter(BankClass.BankName == name).first().StaffofBank) == 0):
            self.session.delete(self.session.query(BankClass).filter(BankClass.BankName == name).first())
        self.session.commit()

'''
class Staff:
    def __init__(self, session):
        self.session = session

    def getStaffbyID(self, id = '', ):
        
'''



if __name__ == '__main__':
    #bank类的接口示例
    engine = db.create_engine('mysql+mysqlconnector://root:2161815@localhost:3306/test')
    DBSession = sessionmaker(bind=engine)
    bank = Bank(DBSession())
    #添加支行信息
    bank.newBank('下北泽支行', '下北泽', 43962800)
    bank.newBank('合肥支行', '合肥', 1919810)
    bank.newBank('济南支行', '济南', 114514)
    #获取按资产顺序排序的银行列表
    print(bank.getBank(orderby='Property'))
    #银行资产修改
    bank.setBank('济南支行', 11400, 'Property')
    #获取列表函数可选参数name、city、propertylow（下界）和propertyhigh（上界）
    print(bank.getBank(city='济南',propertylow=1000,propertyhigh=1000000,orderby='City'))
    #根据name（primary key）删除支行
    bank.delBank('济南支行')
    print(bank.getBank())
    
