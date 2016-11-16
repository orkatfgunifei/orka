#coding: utf-8
from flask import g, redirect, url_for, request
from flask.ext.appbuilder import ModelView, expose, has_access
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.orm.attributes import get_history
from app.api.orka import (
    create_container, remove_container, status_container,
    inspect_container, rename_container, list_containers,
    create_object
)

from app.models.container import Container, ContainerType
from flask.ext.babel import lazy_gettext as _


class ContainerModelView(ModelView):

    datamodel = SQLAInterface(Container)
    route_base = '/container'
    #default_view = 'container'

    @expose('/dashboard')
    @has_access
    def container(self):

        self.update_redirect()

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

        if not len(containers) > 0:
            return redirect(url_for('ContainerModelView.add'))

        return self.render_template('orka/container/base.html',
                                    appbuilder=self.appbuilder,
                                    containers=containers
                                    )

    list_title = _("List Container")

    show_title = _("Show Container")

    add_title = _("Add Container")

    edit_title = _("Edit Container")

    label_columns = {'name': _('Name'),
                     'image': _('Image'),
                     'port': _('Port'),
                     'hash_id': _('ID Container'),
                     'domain_name': _('Domain Name'),
                     'cpu_reserved': _('CPU Reserved'),
                     'storage_reserved': _('Storage Reserved'),
                     'status': _('Status'),
                     'type': _('Type'),
                     'linked': _('Linked'),
                     'volumes': _('Volumes Binding'),
                     'environment': _('Environment Variables'),
                     'command': _('Command'),
                     'extra_params': _("Extra Parameters"),
                     'ip': _('IP'),
                     'ip_url': _('IP Adrress')
                     }

    list_columns = ['name',
                    'image',
                    'ip_url',
                    'port',
                    'status',
                    ]

    show_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'image',
                        'ip_url',
                        'port',
                        'status'
                               ]}),
        (
            _('Advanced Info'),
            {'fields': [
                        'type',
                        'linked',
                        'hash_id',
                        'environment',
                        'volumes',
                        'command',
                        'extra_params',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved'], 'expanded': False}),
    ]

    add_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'image',
                        'port'
                               ]}),
        (
            _('Advanced Info'),
            {'fields': [
                        'type',
                        'linked',
                        'environment',
                        'volumes',
                        'command',
                        'extra_params',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved'], 'expanded': True}),
    ]

    edit_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'image',
                        'port',
                        'status']}),
        (
            _('Advanced Info'),
            {'fields': [
                        'type',
                        'linked',
                        'ip',
                        'hash_id',
                        #'environment',
                        #'volumes',
                        #'command',
                        #'extra_params',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved'], 'expanded': False}),
    ]

    search_columns = [
        'name',
        'image',
        'ip',
        'port',
        'status',
        'type',
        'hash_id',
        'domain_name',
        'cpu_reserved',
        'storage_reserved',
        'linked'
    ]



    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do container
        :param item: objeto Container definido em models
        :return:
        """
        super(ContainerModelView, self).pre_add(item)

        if g.user.is_authenticated():
            item.user_id = g.user.id

            container = create_container(item)

            if not container.get('Id'):
                raise RuntimeError("Não foi possível criar o container [%s]" % (item.name))
            elif container.get('urubu'):
                item.hash_id = container.get('Id')
                item.status = container.get('running')
            else:
                item.hash_id = container.get('Id')
                status_container(True, item.hash_id)
                item.status = True

            inspect = inspect_container(container.get('Id'))

            if not item.name:
                item.name = inspect.get('Name')

            if container.get('ip_address'):
                item.ip = container.get('ip_address')
            else:

                try:
                    if inspect['State']['Status'] == 'running':
                        item.status = True

                    if inspect.get('NetworkSettings'):
                        ip_address = inspect['NetworkSettings']['Networks']['bridge']['IPAddress']

                        item.ip = ip_address
                except:
                    item.ip = None
                    item.status = False

    def pre_delete(self, item):
        """
        Antes de remover o container do banco
        mata o processo e remove
        :param item: objeto Container
        :return:
        """
        super(ContainerModelView, self).pre_delete(item)

        if item.hash_id:
            status_container(False, item.hash_id)
            remove_container(item.hash_id)


    def pre_update(self, item):
        """
        Antes de atualizar o container no banco
        renomeia o container e altera as demais modificações
        :param item: objeto Container
        :return:
        """
        super(ContainerModelView, self).pre_update(item)
        #len(old_name.unchanged)
        container = self.appbuilder.session.query(Container).get(item.id)

        # Verfica cada parâmetro por mudanças
        name = get_history(container, 'name')

        if not len(name.unchanged) > 0:
            rename_container(item.hash_id, name.added[0])

        status = get_history(container, 'status')

        if not len(status.unchanged) > 0:
            action = bool(status.added[0])

            status_container(action, item.hash_id)

            if not action:
                """
                Ação Desligar Container
                """
                container.ip = None
            else:
                """
                Ação Ligar Container
                """
                info_container = inspect_container(container.hash_id)

                if info_container.get('NetworkSettings'):
                    ip_address = info_container['NetworkSettings']['Networks']['bridge']['IPAddress']
                    container.ip = ip_address

            if self.appbuilder.session.dirty:
                self.appbuilder.session.commit()


