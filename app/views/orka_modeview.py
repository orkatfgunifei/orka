#coding: utf-8
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder import

class RenderTemplateOrkaWidget(object):
    """
        Base template for every widget
        Enables the possibility of rendering a template
         inside a template with run time options
    """
    template = 'appbuilder/general/widgets/render.html'


class ListOrka(RenderTemplateOrkaWidget):
    """
        List Widget implements a Template as an widget.
        It takes the following arguments

        label_columns = []
        include_columns = []
        value_columns = []
        order_columns = []
        page = None
        page_size = None
        count = 0
        pks = []
        actions = None
        filters = {}
        modelview_name = ''
    """
    template = 'orka/general/widgets/list.html'


class OrkaModelView(ModelView):

    list_template = 'orka/general/model/list.html'

    edit_template = 'orka/general/model/edit.html'

    add_template = 'orka/general/model/add.html'

    show_template = 'orka/general/model/show.html'

    list_widget = ListOrka
    """ List widget override """
    edit_widget = FormWidget
    """ Edit widget override """
    add_widget = FormWidget
    """ Add widget override """
    show_widget = ShowWidget
    """ Show widget override """

