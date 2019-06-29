import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext

import os
import sys
from sqlalchemy import Column, CHAR, INT, DATE, ForeignKey, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import text

from werkzeug.security import generate_password_hash

engine = create_engine( \
    'mysql+mysqlconnector://root:mayuxin1999@localhost:3306/bankdbms')
DBSession = sessionmaker(bind=engine)



Base = declarative_base()


class BankClass(Base):
    __tablename__ = 'Bank'

    BankName = Column(CHAR(255), primary_key=True, nullable=False)
    City = Column(CHAR(255), nullable=False)
    Property = Column(FLOAT, nullable=False)


class StaffClass(Base):
    __tablename__ = 'Staff'

    StaffID = Column(CHAR(18), primary_key=True, nullable=False)
    BankName = Column(CHAR(255), ForeignKey('Bank.BankName'))
    StaffName = Column(CHAR(18), nullable=False)
    Phone = Column(CHAR(14), nullable=False)
    Address = Column(CHAR(255), nullable=False)
    DateStartWorking = Column(DATE, nullable=False)
    bankname = relationship('BankClass', backref='StaffofBank')


class ClientClass(Base):
    __tablename__ = 'Client'

    ClientID = Column(CHAR(18), primary_key=True, nullable=False)
    ClientName = Column(CHAR(18), nullable=False)
    Phone = Column(CHAR(14), nullable=False)
    Address = Column(CHAR(255), nullable=False)


class AccountClass(Base):
    __tablename__ = 'Account'

    AccountID = Column(CHAR(11), primary_key=True, nullable=True)
    Balance = Column(FLOAT, nullable=True)
    DateOpening = Column(DATE, nullable=True)


class CheckAccountClass(Base):
    __tablename__ = 'CheckAccount'

    AccountID = Column(CHAR(11), ForeignKey('Account.AccountID'), primary_key=True, nullable=True)
    Balance = Column(FLOAT, nullable=True)
    DateOpening = Column(DATE, nullable=True)
    Overdraft = Column(FLOAT)
    accountid = relationship('AccountClass', backref='CheckofAccount', foreign_keys=[AccountID])

class SaveAccountClass(Base):
    __tablename__ = 'SaveAccount'

    AccountID = Column(CHAR(11), ForeignKey('Account.AccountID'), primary_key=True, nullable=True)
    Balance = Column(FLOAT, nullable=True)
    DateOpening = Column(DATE, nullable=True)
    Rate = Column(FLOAT)
    accountid = relationship('AccountClass', backref='SaveofAccount', foreign_keys=[AccountID])


class OwningClass(Base):
    __tablename__ = 'Owning'

    ClientID = Column(CHAR(18), ForeignKey('Client.ClientID'), primary_key=True)
    LoanID = Column(CHAR(18), ForeignKey('Loan.LoanID'), primary_key=True)
    clientid = relationship('ClientClass', backref='OwnofClinet', foreign_keys=[ClientID])
    loanid = relationship('LoanClass', backref='OwnofLoan', foreign_keys=[LoanID])


class LinkManClass(Base):
    __tablename__ = 'LinkMan'

    ClientID = Column(CHAR(18), ForeignKey('Client.ClientID'), primary_key=True, nullable=True)
    LinkName = Column(CHAR(16), primary_key=True, nullable=True)
    Phone = Column(CHAR(14))
    Email = Column(CHAR(14))
    Association = Column(CHAR(128))
    clientid = relationship('ClientClass', backref='LinkofClient', foreign_keys=[ClientID])


class LoanClass(Base):
    __tablename__ = 'Loan'

    LoanID = Column(CHAR(18), primary_key=True)
    BankName = Column(CHAR(255), ForeignKey('Bank.BankName'))
    Amount = Column(FLOAT, nullable=True)
    clientid = relationship('BankClass', backref='LoanofBank')


class PayLoanClass(Base):
    __tablename__ = 'PayLoan'

    PayID = Column(CHAR(18), primary_key=True)
    LoanID = Column(CHAR(18), ForeignKey('Loan.LoanID'), primary_key=True)
    Date = Column(DATE)
    Amount = Column(FLOAT, nullable=False)
    loanid = relationship('LoanClass', backref='PayofLoan')


class OpenAccountClass(Base):
    __tablename__ = 'OpenAccount'

    BankName = Column(CHAR(255), ForeignKey('Bank.BankName'), primary_key=True)
    ClientID = Column(CHAR(18), ForeignKey('Client.ClientID'), primary_key=True)
    CheckAccountID = Column(CHAR(11), ForeignKey('CheckAccount.AccountID'))
    SaveAccountID = Column(CHAR(11), ForeignKey('SaveAccount.AccountID'))
    bankname = relationship('BankClass', backref='AccountofBank', foreign_keys=[BankName])
    clientid = relationship('ClientClass', backref='AccountofCilent', foreign_keys=[ClientID])
    checkaccountid = relationship('CheckAccountClass', backref='OpenofCheck', foreign_keys=[CheckAccountID])
    saveaccountid = relationship('SaveAccountClass', backref='OpenofSave', foreign_keys=[SaveAccountID])


class PersonInChargeClass(Base):
    __tablename__ = 'PersonInCharge'

    ClientID = Column(CHAR(18), ForeignKey('Client.ClientID'), primary_key=True, nullable=False)
    StaffID = Column(CHAR(18), ForeignKey('Staff.StaffID'), primary_key=True, nullable=False)
    clientid = relationship('ClientClass', backref='ChargeofClient', foreign_keys=[ClientID])
    staffid = relationship('StaffClass', backref='ChargeofStaff', foreign_keys=[StaffID])

class UserClass(Base):
    __tablename__ = 'user'

    username = Column(CHAR(255), primary_key=True)
    password = Column(CHAR(255), nullable=False)
    # permissions from 0 to 3
    permissions = Column(INT, nullable=False)

from contextlib import contextmanager

@contextmanager
def session_scope():
    session = DBSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """Clear existing data and create new tables."""
    db = engine.connect()
    Base.metadata.drop_all(engine, checkfirst=True)
    # tables = list(reversed(Base.metadata.sorted_tables))
    # tables = Base.metadata.sorted_tables
    # for table in tables:
    #     table.drop(engine, checkfirst=True)
    Base.metadata.create_all(engine)

    # add admin user
    with session_scope() as db_session:
        db_session.add(UserClass(\
            username="admin", password=generate_password_hash('mayuxin1999'), permissions=3))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
