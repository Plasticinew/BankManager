import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext

import os
import sys
from sqlalchemy import Column, CHAR, INT, DATE, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine( \
    'mysql+mysqlconnector://root:mayuxin1999@localhost:3306/bankdbms')
DBSession = sessionmaker(bind=engine)

Base = declarative_base()

class BankClass(Base):
    __tablename__ = 'Bank'

    BankName = Column(CHAR(255), primary_key=True, nullable=False)
    City = Column(CHAR(255), nullable=False)
    Property = Column(INT, nullable=False)

    # Workers = db.orm.relationship('银行员工')

    def __repr__(self):
        return "<Bank(BankName = '%s', City = '%s', Property = '%d')" \
               % (self.BankName, self.City, self.Property)

class StaffClass(Base):
    __tablename__ = 'Staff'

    StaffID = Column(CHAR(18), primary_key=True, nullable=False)
    BankName = Column(CHAR(255), ForeignKey('Bank.BankName'),nullable=False)
    StaffName = Column(CHAR(18), nullable=False)
    Phone = Column(CHAR(14), nullable=False)
    Address = Column(CHAR(255), nullable=False)
    DateStartWorking = Column(DATE, nullable=False)
    bankname = relationship('BankClass',backref='StaffofBank')

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
    tables = list(reversed(Base.metadata.sorted_tables))
    for table in tables:
        table.drop(engine)
    Base.metadata.create_all(engine)


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
