#coding: utf-8
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask import flash
from app.models.node import Node
from app.views import _, cli


class NodeModelView(ModelView):

    datamodel = SQLAInterface(Node)

    route_base = "/node"

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

        if item.name:

            spec = cli.create_swarm_spec(
                snapshot_interval=5000, log_entries_for_slow_followers=1200
            )
            listen_addr = '%s:%s' % (item.listen_addr, item.listen_port)
            ok = cli.init_swarm(
                advertise_addr='127.0.0.1', listen_addr=listen_addr, force_new_cluster=False,
                swarm_spec=spec
            )
            if ok:
                flash(_("Node Created!"), "info")

    def pre_delete(self, item):

        super(NodeModelView, self).pre_delete(item)

        cli.leave_swarm()