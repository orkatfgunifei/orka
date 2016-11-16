#coding: utf-8
from flask import jsonify
from flask.ext.appbuilder import IndexView, has_access, expose
from flask import g, redirect, url_for, request, redirect, make_response, session
from models.service import Service
from models.container import Container
from models.node import Node
import psutil
from app.api.orka import (
    inspect_container, inspect_service,
    list_containers, create_object
)

class IndexView(IndexView):
    index_template = 'index.html'

    @expose('/')
    def index(self):
        if g.user.is_authenticated():

            containers = self.appbuilder.session.query(Container).all()

            host_containers = list_containers(list_all=True)

            for host_container in host_containers:
                if host_container.get('CONTAINER ID') == 'CONTAINER ID':
                    host_containers.pop(host_containers.index(host_container))
                if not host_container.get('NAMES'):
                    host_containers.pop(host_containers.index(host_container))

            in_host = False

            for container in containers:

                try:
                    for host_container in host_containers:
                        if host_container.get('CONTAINER ID') in container.hash_id:
                            host_containers.pop(host_containers.index(host_container))
                            in_host = True

                    if in_host:

                        info_container = inspect_container(container.hash_id)

                        status = info_container.get('State')

                        if not status['Running'] and container.status:
                            #containers.pop(index_container)
                            container.status = False
                            container.ip = None
                        elif status['Running'] and not container.status:
                            container.status = True

                            if info_container.get('NetworkSettings'):
                                ip_address = info_container['NetworkSettings']['Networks']['bridge']['IPAddress']
                                container.ip = ip_address
                    else:

                        self.appbuilder.session.delete(container)
                        self.appbuilder.session.commit()


                except:
                    container.status = False

                in_host = False

            for host_container in host_containers:

                stat = False

                if host_container.get('CONTAINER ID'):
                    info_container = inspect_container(host_container.get('CONTAINER ID'))

                    status = info_container.get('State')

                    if not status['Running']:
                        stat = False
                        ip_addr = None
                    else:
                        stat = True

                        if info_container.get('NetworkSettings'):
                            ip_addr = info_container['NetworkSettings']['Networks']['bridge']['IPAddress']

                    objeto = {
                        'name': host_container.get('NAMES'),
                        'hash_id': host_container.get('CONTAINER ID'),
                        'command': host_container.get('COMMAND'),
                        'status': stat,
                        'image': host_container.get('IMAGE'),
                        'ip': ip_addr or None,
                    }

                    new_container = create_object("Container", objeto, self.appbuilder)
                    containers.append(new_container)

            if self.appbuilder.session.dirty:
                self.appbuilder.session.commit()

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

            containers = self.appbuilder.session.query(Container).filter(Container.name.like("%" + data + "%")).all()

        for container in containers:

            try:

                info_container = inspect_container(container.hash_id)

                status = info_container.get('State')

                if not status['Running'] and container.status:
                    # containers.pop(index_container)
                    container.status = False
                    container.ip = False
                elif status['Running'] and not container.status:
                    container.status = True

                    if info_container.get('NetworkSettings'):
                        ip_address = info_container['NetworkSettings']['Networks']['bridge']['IPAddress']
                        container.ip = ip_address

            except:
                container.status = False

        if not data:
            services = self.appbuilder.session.query(Service).filter_by(created_by=g.user).all()
        else:
            services = self.appbuilder.session.query(Service).filter(Service.name.like("%" + data + "%")).all()

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
            nodes = self.appbuilder.session.query(Node).filter(Node.name.like("%" + data + "%")).all()

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

