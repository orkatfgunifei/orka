#coding: utf-8

from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from app.models.image import Image
from container import ContainerModelView

class ImageModelView(ModelView):
    datamodel = SQLAInterface(Image)

    related_views = [ContainerModelView]

    list_columns = ['name']

    base_order = ('name', 'asc')