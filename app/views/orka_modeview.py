#coding: utf-8
from flask.ext.appbuilder import ModelView

class OrkaModelView(ModelView):

    list_template = 'orka/general/model/list.html'

    edit_template = 'orka/general/model/edit.html'

    add_template = 'orka/general/model/add.html'

    show_template = 'orka/general/model/show.html'

