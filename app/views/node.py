#coding: utf-8
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface

from app.models.node import Node
from container import ContainerModelView, _


class NodeModelView(ModelView):

    datamodel = SQLAInterface(Node)

    route_base = "/node"

    related_views = [ContainerModelView]

    list_title = _("List Node")

    show_title = _("Show Node")

    add_title = _("Add Node")

    edit_title = _("Edit Node")

    label_columns = {'name': _('Name'),
                     'remote_addr': _('Remote IP'),
                     'remote_port': _('Remote Port'),
                     'listen_addr': _('Listen IP'),
                     'listen_port': _('Listen Port'),
                     'join_token': _('Join Token')
                     }

    list_columns = ['name', 'remote_addr', 'remote_port', 'listen_addr', 'listen_port']

    show_fieldsets = [
        (_('Node Options'), {'fields': [
                        'name',
                        'remote_addr',
                        'remote_port',
                        'listen_addr',
                        'listen_port'
                               ]}),
    ]

    add_fieldsets = [
        (_('Node Options'), {'fields': [
                        'name',
                        'remote_addr',
                        'remote_port',
                        'listen_addr',
                        'listen_port',
                        'join_token'
                               ]}),
    ]

    edit_fieldsets = [
        (_('Node Options'), {'fields': [
                        'name',
                        'remote_addr',
                        'remote_port',
                        'listen_addr',
                        'listen_port',
                        'join_token'
                               ]}),
    ]

    search_fieldsets = [
        (_('Node Options'), {'fields': [
                        'name',
                        'remote_addr',
                        'remote_port',
                        'listen_addr',
                        'listen_port',
                        'join_token'
                               ]}),
    ]

    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do nó
        :param item: objeto Node definido em models
        :return:
        """
        super(NodeModelView, self).pre_add(item)

        # TODO: https://docker-py.readthedocs.io/en/latest/swarm/ Estudar
        if item.name:
            print "Implemente o criar !"