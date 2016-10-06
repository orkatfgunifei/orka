#coding: utf-8

"""
    Inicializador da montagem das visões
"""

import logging
from flask import render_template
from flask.ext.babelpkg import lazy_gettext as _
from flask_appbuilder.models.mixins import UserExtensionMixin
from app import db, appbuilder

from container import ContainerModelView
from contact import ContactModelView, ContactChartView, ContactTimeChartView, GroupModelView, fill_gender
from images import ImageModelView
from node import NodeModelView
#from logs import LogsView

# Início Log
log = logging.getLogger(__name__)



"""
    Controlador de erro 404
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()

fill_gender()

appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", category="Contacts", category_icon='fa-envelope', label=_("Contacts"))
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts", label=_("List Contacts"))
appbuilder.add_separator("Contacts")
appbuilder.add_view(ContactChartView, "Contacts Chart", icon="fa-dashboard", category="Contacts", label=_("Contacts Chart"))
appbuilder.add_view(ContactTimeChartView, "Contacts Birth Chart", icon="fa-dashboard", category="Contacts", label=_("Contacts Birth Chart"))
appbuilder.add_view(ImageModelView, "List Images", icon="fa-hdd-o", label=_('Images'))
appbuilder.add_view(ContainerModelView, "List Container", icon="fa-database", label=_('Containers'))
appbuilder.add_view(NodeModelView, "List Node", icon='fa-sitemap', label=_('Nodes'))
#appbuilder.add_view(LogsView, "Logs", icon='fa-align-left ', label=_('Logs'))

log.info("Flask Appbuilder Versão: {0}".format(appbuilder.version))
log.info("Classe de extensão usuário {0}".format(UserExtensionMixin.__subclasses__()[0]))
