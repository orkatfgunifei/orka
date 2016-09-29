#coding: utf-8

import logging
from flask import Flask
from flask.ext.appbuilder import SQLA, AppBuilder
from app.index import IndexView
from app.api.docker import Docker

"""
 Configuração de log
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

# Instância do cliente Docker
cli = Docker()

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, indexview=IndexView)




"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""    

from app import models, views

