import calendar
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder.charts.views import GroupByChartView
from flask.ext.appbuilder.models.group import aggregate_count
from flask.ext.babelpkg import lazy_gettext as _
from flask_appbuilder.security.views import UserDBModelView

from app import db, appbuilder
from .models import OrkaUser, Image, Node, Container

class UserModelView(UserDBModelView):
    
    def __init__(self):
        super(UserModelView, self).__init__()
    
    datamodel = SQLAInterface(OrkaUser)
    
    show_fieldsets = [
        (_('User info'),
         {'fields': ['username', 'active', 'roles', 'login_count', 'personal_phone']}),
        (_('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
        (_('Audit Info'),
         {'fields': ['last_login', 'fail_login_count', 'created_on',
                     'created_by', 'changed_on', 'changed_by'], 'expanded': False}),
    ]

    user_show_fieldsets = [
        (_('User info'),
         {'fields': ['username', 'active', 'roles', 'login_count', 'personal_phone']}),
        (_('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
    ]

    add_columns = ['first_name', 'last_name', 'username', 'active', 'email', 'roles', 'personal_phone', 'password', 'conf_password']
    list_columns = ['first_name', 'last_name', 'username', 'email', 'active', 'roles']
    edit_columns = ['first_name', 'last_name', 'username', 'active', 'email', 'roles', 'personal_phone']

class ContainerModelView(ModelView):
    datamodel = SQLAInterface(Container)

    list_columns = ['name', 
                    'hostname', 
                    'host', 
                    'domain_name', 
                    'cpu_reserved',
                    'storage_reserved', 
                    'environment', 
                    'image',
                    'node',
                    'container_type',
                    'docker_file']

   

    show_fieldsets = [
        ('Summary', {'fields': [
                        'name', 
                        'domain_name', 
                        'container_type'
                               ]}),
        (
            'Advanced Info',
            {'fields': [     
                        'hostname',
                        'host', 
                        'domain_name', 
                        'cpu_reserved',
                        'storage_reserved', 
                        'environment', 
                        'image',
                        'node',
                        'docker_file'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': [
                        'name', 
                        'domain_name', 
                        'container_type'
                               ]}),
        (
            'Advanced Info',
            {'fields': [     
                        'hostname',
                        'host', 
                        'domain_name', 
                        'cpu_reserved',
                        'storage_reserved', 
                        'environment', 
                        'image',
                        'node',
                        'docker_file'], 'expanded': True}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': [
                        'name', 
                        'domain_name', 
                        'container_type'
                               ]}),
        (
            'Advanced Info',
            {'fields': [     
                        'hostname',
                        'host', 
                        'domain_name', 
                        'cpu_reserved',
                        'storage_reserved', 
                        'environment', 
                        'image',
                        'node',
                        'docker_file'], 'expanded': False}),
    ]
    
    search_fieldsets = [
        ('Summary', {'fields': [
                        'name', 
                        'domain_name', 
                        'container_type'
                               ]}),
        (
            'Advanced Info',
            {'fields': [     
                        'hostname',
                        'host', 
                        'domain_name', 
                        'cpu_reserved',
                        'storage_reserved', 
                        'environment', 
                        'image',
                        'node',
                        'docker_file'], 'expanded': False}),
    ]

class NodeModelView(ModelView):
    datamodel = SQLAInterface(Node)
    related_views = [ContainerModelView]
    
class ImageModelView(ModelView):
    datamodel = SQLAInterface(Image)

    list_columns = ['name']

    base_order = ('name', 'asc')

#    show_fieldsets = list_columns
#
#    add_fieldsets = list_columns
#
#    edit_fieldsets = list_columns
#    


db.create_all()
appbuilder.add_view(UserModelView, "List User", icon="fa-user", label=_('Users'))
appbuilder.add_view(ImageModelView, "List Images", icon="fa-hdd-o", label=_('Images'))
appbuilder.add_view(ContainerModelView, "List Container", icon="fa-database", label=_('Containers'))
appbuilder.add_view(NodeModelView, "List Node", icon='fa-sitemap', label=_('Nodes'))


