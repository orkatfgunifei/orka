#coding: utf-8

from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from app.models.node import Node
from container import ContainerModelView
from app import cli

class NodeModelView(ModelView):
    datamodel = SQLAInterface(Node)

    related_views = [ContainerModelView]

    list_columns = ['name', 'ip']

    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do nó
        :param item: objeto Node definido em models
        :return:
        """
        super(NodeModelView, self).pre_add(item)

        if item.name:

            endpoint_config = cli.create_endpoint_config(
                aliases=[item.name],
                ipv4_address=item.ip
            )

            node_id = cli.create_network(item.name)

            if node_id.get('Id'):
                item.node_id = node_id['Id']

            item.networking_config = cli.create_networking_config({
                item.name: endpoint_config
            })