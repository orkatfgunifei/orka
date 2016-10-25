#coding: utf-8
import flask
from flask import g, redirect, url_for, request, redirect, make_response, session
from flask.ext.appbuilder import BaseView, expose, has_access
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface


from app.models.container import Container
from flask.ext.babel import lazy_gettext as _


class DashboardModelView(BaseView):
    #
    datamodel = SQLAInterface(Container)
    route_base = '/dashboard'

    @expose('/dashboard', methods=['GET'])
    @has_access
    def dashboard(self):

        self.update_redirect()
        json = {'chave': 'valor'}
        # TODO: Informações do sistema para o json, requisição se repete a cada 2,5 segundos no FrontEnd
        # return session(flask.jsonify(json))
        # containers = db.session.query(Container).all()

        # if not len(containers) > 0:
        #     return redirect(url_for('ContainerModelView.add'))
        return self.render_template('orka/dashboard.html')