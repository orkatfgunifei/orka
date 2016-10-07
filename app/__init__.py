#coding: utf-8

import logging
from flask import Flask
from flask.ext.appbuilder import SQLA, AppBuilder
from app.index import IndexView
from docker import Client

"""
 Configuração de log
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

# Instância do cliente Docker
cli = Client(base_url='unix://var/run/docker.sock')

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
# appbuilder = AppBuilder(app, db.session, base_template='orkabase.html')
appbuilder = AppBuilder(app, db.session, indexview=IndexView)

appbuilder.base_template='orka/baselayout.html'


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

