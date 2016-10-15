#coding: utf-8
import flask
from flask.ext.appbuilder import IndexView, has_access, expose
from flask import g, redirect, url_for, request, redirect, make_response, session

class IndexView(IndexView):
    index_template = 'index.html'

    # TODO: Informações do sistema para o json, requisição se repete a cada 2,5 segundos no FrontEnd##
    @expose('/usage', methods=['GET'])
    @has_access
    def dashboard(self):
        self.update_redirect()
        json = {'chave': 'valor'}

        return flask.jsonify(json)



