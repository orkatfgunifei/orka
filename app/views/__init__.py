#coding: utf-8

"""
    Inicializador da montagem das visões
"""

import logging
from flask import render_template, make_response
from flask.ext.babel import lazy_gettext as _
from flask.ext.appbuilder import BaseView, expose, has_access

from service import ServiceView, db, appbuilder
from container import ContainerModelView
from image import ImageModelView
from node import NodeModelView




# Início Log
log = logging.getLogger(__name__)



"""
    Controlador de erro 404
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

db.create_all()

appbuilder.add_link("Dashboard", label=_("Dashboard"), href='/', icon='fa-home')
appbuilder.add_view(ServiceView, "Servidbces", label=_('Services'), icon='fa-server')
appbuilder.add_view(ContainerModelView, "Container", label=_('Container'), icon='fa-database')
appbuilder.add_view(ImageModelView, "Images", label=_('Images'), icon='fa-hdd-o')
appbuilder.add_view(NodeModelView, "Nodes", icon='fa-sitemap', label=_('Nodes'))

security = appbuilder.sm

active_views = [
    "Service",
    "Container",
    "Image",
    "Images",
    "Dashboard",
    "UserInfoEditView",
    "ResetPasswordView",
    "ResetMyPasswordView",
    "OrkaUserDBView"
]

allroles = security.get_all_roles()
roles = [str(x) for x in allroles]
admin_role = allroles[0]

if not "User" in roles:
    user_role = security.add_role("User")

    for perm in admin_role.permissions:
        for view in active_views:
            if (view in str(perm)):
                security.add_permission_role(user_role, perm)
                print "[Security] Permissão de Usuário: ", perm



log.info("Flask-Appbuilder Versão: {0}".format(appbuilder.version))
