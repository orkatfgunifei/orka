import calendar
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder.charts.views import GroupByChartView
from flask.ext.appbuilder.models.group import aggregate_count
from flask.ext.babelpkg import lazy_gettext as _


from app import db, appbuilder
from .models import User, Image, Node, Container

class UserModelView(ModelView):
    datamodel = SQLAInterface(User)

    list_columns = ['name', 'username', 'email']

    base_order = ('name', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': ['name']}),
        (
            'Personal Info',
            {'fields': ['email', 'personal_phone'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['name', 'username', 'email']}),
        (
            'Personal Info',
            {'fields': ['personal_phone'], 'expanded': False}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['name']}),
        (
            'Personal Info',
            {'fields': ['email', 'personal_phone'], 'expanded': False}),
    ]

class ContainerModelView(ModelView):
    datamodel = SQLAInterface(Container)

    list_columns = ['name', 
                    'hostname', 
                    'port',
                    'host', 
                    'domain_name', 
                    'cpu_reserved',
                    'storage_reserved', 
                    'environment', 
                    'image',
                    'node',
                    'container_type',
                    'docker_file']

    base_order = ('name', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': [
                        'name', 
                        'hostname', 
                        'container_type'
                               ]}),
        (
            'Advanced Info',
            {'fields': [     
                        'port',
                        'host', 
                        'domain_name', 
                        'cpu_reserved',
                        'storage_reserved', 
                        'environment', 
                        'image',
                        'node',
                        'docker_file'], 'expanded': False}),
    ]

    #add_fieldsets = show_fieldsets

    #edit_fieldsets = show_fieldsets

class NodeModelView(ModelView):
    datamodel = SQLAInterface(Node)
    related_views = [ContainerModelView]
    
class ImageModelView(ModelView):
    datamodel = SQLAInterface(Image)

    list_columns = ['name', 'virtual_size']

    base_order = ('name', 'asc')

#    show_fieldsets = list_columns
#
#    add_fieldsets = list_columns
#
#    edit_fieldsets = list_columns
#    


db.create_all()
appbuilder.add_view(UserModelView, "List User", icon="fa-user", label=_('Users'))
appbuilder.add_view(NodeModelView, "List Node", icon='fa-sitemap', label=_('Nodes'))
appbuilder.add_view(ImageModelView, "List Images", icon="fa-hdd-o", label=_('Images'))
appbuilder.add_view(ContainerModelView, "List Container", icon="fa-database", label=_('Containers'))


