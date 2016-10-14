#coding: utf-8
import random
import time
import logging
from flask import Flask, url_for, jsonify, render_template, session, request, flash, redirect
#from flask.ext.mail import Mail
from flask.ext.appbuilder import SQLA, AppBuilder
from index import IndexView
from security import OrkaSecurityManager
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

#mail = Mail(app)


db = SQLA(app)

appbuilder = AppBuilder(app, db.session, indexview=IndexView, security_manager_class=OrkaSecurityManager)

appbuilder.base_template='orka/baselayout.html'

#appbuilder.security_cleanup()

from sqlalchemy.engine import Engine
from sqlalchemy import event


#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

from app import models, views

