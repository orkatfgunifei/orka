#coding: utf-8
import random
import time
import logging
from flask import Flask, url_for, jsonify, render_template, session, request, flash, redirect
from flask.ext.mail import Mail, Message
from flask.ext.appbuilder import SQLA, AppBuilder
from index import IndexView
from security import OrkaSecurityManager
from docker import Client
from tasks import make_celery, task, long_task

"""
 Configuração de log
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

# Instância do cliente Docker
cli = Client(base_url='unix://var/run/docker.sock')

app = Flask(__name__)
app.config.from_object('config')

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

mail = Mail(app)

celery = make_celery(app)

db = SQLA(app)

appbuilder = AppBuilder(app, db.session, indexview=IndexView, security_manager_class=OrkaSecurityManager)

appbuilder.base_template='orka/baselayout.html'

@task(name='orka.app.send_async_email')
def send_async_email(msg):
    """Tarefa em Background para envios de msgs via Flask-Mail."""
    with app.app_context():
        mail.send(msg)

@app.route('/async', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('async.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    msg = Message('Hello from Flask',
                  recipients=[request.form['email']])
    msg.body = 'This is a test email sent from a background Celery task.'
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(msg)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[msg], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

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

