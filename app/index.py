#coding: utf-8
from flask import jsonify
from flask.ext.appbuilder import IndexView, has_access, expose
from flask import g, redirect, url_for, request, redirect, make_response, session
from models.service import Service
from models.container import Container
from models.node import Node
import psutil
from app.api.orka import inspect_container, inspect_service

class IndexView(IndexView):
    index_template = 'index.html'

    @expose('/')
    def index(self):
        if g.user.is_authenticated():
            containers = self.appbuilder.session.query(Container).filter_by(created_by=g.user).all()

            for container in containers:

                try:

                    info_container = inspect_container(container.hash_id)

                    status = info_container.get('State')

                    if not status['Running'] and container.status:
                        # containers.pop(index_container)
                        container.status = False
                    elif status['Running'] and not container.status:
                        container.status = True

                except:
                    container.status = False

            services = self.appbuilder.session.query(Service).filter_by(created_by=g.user).all()

            for service in services:

                try:
                    info_service = inspect_service(service.service_id)

                    if info_service and not service.status:
                        service.status = True
                except:
                    service.status = False

            if self.appbuilder.session.dirty:
                self.appbuilder.session.commit()

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

    @expose('/search', methods=['POST'])
    @has_access
    def search(self):

        data = request.form["q"]

        if not data:
            containers = self.appbuilder.session.query(Container).filter_by(created_by=g.user).all()
        else:
            containers = self.appbuilder.session.query(Container).filter_by(name=data).all()

        for container in containers:

            try:

                info_container = inspect_container(container.hash_id)

                status = info_container.get('State')

                if not status['Running'] and container.status:
                    # containers.pop(index_container)
                    container.status = False
                elif status['Running'] and not container.status:
                    container.status = True

            except:
                container.status = False

        if not data:
            services = self.appbuilder.session.query(Service).filter_by(created_by=g.user).all()
        else:
            services = self.appbuilder.session.query(Service).filter_by(name=data).all()

        for service in services:

            try:
                info_service = inspect_service(service.service_id)

                if info_service and not service.status:
                    service.status = True
            except:
                service.status = False

        if self.appbuilder.session.dirty:
            self.appbuilder.session.commit()

        if not data:
            nodes = self.appbuilder.session.query(Node).all()
        else:
            nodes = self.appbuilder.session.query(Node).filter_by(name=data).all()

        self.update_redirect()

        return self.render_template(self.index_template,
                                    appbuilder=self.appbuilder,
                                    containers=containers,
                                    services=services,
                                    nodes=nodes
                                    )


    # TODO: Informações do sistema para o json, requisição se repete a cada 2,5 segundos no FrontEnd##
    @expose('/usage', methods=['GET'])
    @has_access
    def usage(self):

        cpu = psutil.cpu_percent()
        disk = psutil.disk_usage('/')[3]
        mem = psutil.virtual_memory()[2]

        dados_dict = {
            'cpu': cpu,
            'disk': disk,
            'ram': mem
        }
        return jsonify(dados_dict)

