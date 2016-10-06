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

        # TODO: https://docker-py.readthedocs.io/en/latest/swarm/ Estudar
        if item.name:
            cli.create_network