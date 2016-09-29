#coding: utf-8

from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from app.models.image import Image

class ImageModelView(ModelView):
    datamodel = SQLAInterface(Image)

    list_columns = ['name']

    base_order = ('name', 'asc')