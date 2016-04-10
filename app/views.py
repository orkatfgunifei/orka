
import logging
import calendar
from flask import flash, render_template
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder.charts.views import GroupByChartView
from flask.ext.appbuilder.models.group import aggregate_count
from flask.ext.babelpkg import lazy_gettext as _
from flask_appbuilder.models.mixins import UserExtensionMixin
from flask_appbuilder import SimpleFormView

from app import db, appbuilder
from .models import Contact, ContactGroup, Gender, Image, Node, Container
from .forms import Terminal
from .index import TerminalForm

log = logging.getLogger(__name__)


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()
        


class ContactModelView(ModelView):
    
    datamodel = SQLAInterface(Contact)

    label_columns = {'contact_group': 'Contacts Group'}
    list_columns = ['name', 'personal_celphone', 'birthday', 'contact_group']

    base_order = ('name', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]


class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]


class ContactChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)
    chart_title = 'Grouped contacts'
    label_columns = ContactModelView.label_columns
    chart_type = 'PieChart'

    definitions = [
        {
            'group' : 'contact_group',
            'series' : [(aggregate_count,'contact_group')]
        },
        {
            'group' : 'gender',
            'series' : [(aggregate_count,'contact_group')]
        }
    ]


def pretty_month_year(value):
    return calendar.month_name[value.month] + ' ' + str(value.year)

def pretty_year(value):
    return str(value.year)


class ContactTimeChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)

    chart_title = 'Grouped Birth contacts'
    chart_type = 'AreaChart'
    label_columns = ContactModelView.label_columns
    definitions = [
        {
            'group' : 'month_year',
            'formatter': pretty_month_year,
            'series': [(aggregate_count,'contact_group')]
        },
        {
            'group': 'year',
            'formatter': pretty_year,
            'series': [(aggregate_count,'contact_group')]
        }
    ]
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
    
    list_columns = ['name', 'ip']
    
    
class ImageModelView(ModelView):
    datamodel = SQLAInterface(Image)

    list_columns = ['name']

    base_order = ('name', 'asc')


class TerminalView(TerminalForm):
    form = Terminal
    form_title = 'Terminal'
    message = 'Terminal exit'

    def form_get(self, form):
        form.bash.data = 'Bem vindo ao terminal'

    def form_post(self, form):
        # post process form
        #form.bash.data = form.comando.data 
        print "Post Terminal"



"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()

fill_gender()
appbuilder.add_view(TerminalView, "Terminal View", icon="fa-group", label=_('Open console terminal'),
                     category="Terminal", category_icon="fa-cogs")
appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", category="Contacts", category_icon='fa-envelope')
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_separator("Contacts")
appbuilder.add_view(ContactChartView, "Contacts Chart", icon="fa-dashboard", category="Contacts")
appbuilder.add_view(ContactTimeChartView, "Contacts Birth Chart", icon="fa-dashboard", category="Contacts")
appbuilder.add_view(ImageModelView, "List Images", icon="fa-hdd-o", label=_('Images'))
appbuilder.add_view(ContainerModelView, "List Container", icon="fa-database", label=_('Containers'))
appbuilder.add_view(NodeModelView, "List Node", icon='fa-sitemap', label=_('Nodes'))


log.info("F.A.B. Version: {0}".format(appbuilder.version))
log.info("User extension class {0}".format(UserExtensionMixin.__subclasses__()[0]))

