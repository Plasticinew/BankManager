import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine( \
    'mysql+mysqlconnector://root:mayuxin1999@localhost:3306/bankdbms')
DBSession = sessionmaker(bind=engine)

Base = declarative_base()


class Bank(Base):
    __tablename__ = 'Bank'

    BankName = Column(String(255), primary_key=True, nullable=False)
    City = Column(String(255), nullable=False)
    Property = Column(Integer, nullable=False)

    # Workers = db.orm.relationship('银行员工')

    def __repr__(self):
        return "<Bank(BankName = '%s', City = '%s', Property = '%d')" \
               % (self.BankName, self.City, self.Property)

def get_dbSession():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = DBSession()

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


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
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
