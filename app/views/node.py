#coding: utf-8

from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from app.models.node import Node
from container import ContainerModelView

class NodeModelView(ModelView):
    datamodel = SQLAInterface(Node)
    related_views = [ContainerModelView]

    list_columns = ['name', 'ip']