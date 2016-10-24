#coding: utf-8
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask import flash
from app.models.node import Node
from app.views import _, cli
from service import ServiceModelView
from app.orka_docker import create_node

class NodeModelView(ModelView):

    datamodel = SQLAInterface(Node)

    route_base = "/node"

    list_title = _("List Node")

    show_title = _("Show Node")

    add_title = _("Add Node")

    edit_title = _("Edit Node")

    related_views = [ServiceModelView]

    label_columns = {'name': _('Name'),
                     'advertise_addr': _('IP Host Docker'),
                     'remote_addr': _('Remote IP'),
                     'remote_port': _('Remote Port'),
                     'listen_addr': _('Listen IP'),
                     'listen_port': _('Listen Port'),
                     'join_token': _('Join Token'),
                     'snapshot_interval': _('Snapshot Interval'),
                     'log_entries_for_slow_followers': _('Logs Slow Followers')
                     }

    list_columns = ['name', 'remote_addr', 'remote_port', 'listen_addr', 'listen_port']

    show_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'advertise_addr',
                        'listen_addr',
                        'listen_port'
                               ]}),
        (_('Advanced'), {'fields': [
            'join_token',
            'snapshot_interval',
            'log_entries_for_slow_followers',
            'remote_addr',
            'remote_port',
        ], 'expanded': False})
    ]

    add_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'advertise_addr',
                        'listen_addr',
                        'listen_port'
                               ]}),
        (_('Advanced'), {'fields': [
            'snapshot_interval',
            'log_entries_for_slow_followers',
            'remote_addr',
            'remote_port',
        ]})
    ]

    edit_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'advertise_addr',
                        'listen_addr',
                        'listen_port'
                               ]}),
        (_('Advanced'), {'fields': [
            'snapshot_interval',
            'log_entries_for_slow_followers',
            'remote_addr',
            'remote_port',
        ], 'expanded': False})
    ]

    search_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'advertise_addr',
                        'listen_addr',
                        'listen_port'
                               ]}),
        (_('Advanced'), {'fields': [
            'join_token',
            'snapshot_interval',
            'log_entries_for_slow_followers',
            'remote_addr',
            'remote_port',
        ]})
    ]

    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do nó
        :param item: objeto Node definido em models
        :return:
        """
        super(NodeModelView, self).pre_add(item)

        create_node(item)


    def pre_delete(self, item):

        super(NodeModelView, self).pre_delete(item)

        try:
            cli.leave_swarm(force=True)
        except:
            print "Não é um objeto Swarm"