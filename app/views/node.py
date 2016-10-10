#coding: utf-8
from orka_modeview import OrkaModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from container import ContainerModelView
from service import cli, _
from app.models.node import Node


class NodeModelView(ModelView):
    datamodel = SQLAInterface(Node)

    related_views = [ContainerModelView]

    label_columns = {'name': _('Name'),
                     'node_id': _('Node ID'),
                     'ip': _('IP Address'),
                     'network_config': _('Network Configuration')
                     }

    list_columns = ['name', 'ip']

    show_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'node_id',
                        'ip',
                        'network_config'
                               ]}),
    ]

    add_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'ip',
                               ]}),
    ]

    edit_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'node_id',
                        'ip',
                        'network_config'
                               ]}),
    ]

    search_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'node_id',
                        'ip',
                        'network_config'
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
            cli.create_network