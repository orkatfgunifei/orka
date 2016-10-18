#coding: utf-8
from flask import jsonify
from flask.ext.appbuilder import IndexView, has_access, expose
from flask import g, redirect, url_for, request, redirect, make_response, session
from models.service import Service
from models.container import Container
from models.node import Node
from random import randint
class IndexView(IndexView):
    index_template = 'index.html'

    @expose('/')
    def index(self):
        if g.user.is_authenticated():
            containers = self.appbuilder.session.query(Container).filter_by(created_by=g.user).all()
            services = self.appbuilder.session.query(Service).filter_by(created_by=g.user).all()
            nodes = self.appbuilder.session.query(Node).all()
            self.update_redirect()

            return self.render_template(self.index_template,
                                    appbuilder=self.appbuilder,
                                    containers=containers,
                                    services=services,
                                    nodes=nodes
                                    )
        else:
            return self.render_template('orka/landing.html',
                                        appbuilder=self.appbuilder)

    # TODO: Informações do sistema para o json, requisição se repete a cada 2,5 segundos no FrontEnd##
    @expose('/usage', methods=['GET'])
    @has_access
    def usage(self):
        dados_dict = {
            'cpu': {'total': 100, 'used': randint(0,100), 'available': 68},
            'disk': {'total': 100, 'used': 55, 'available': 34},
            'ram': {'total': 100, 'used': 62, 'available': 48}
        }
        return jsonify(dados_dict)

