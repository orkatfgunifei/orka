#coding: utf-8

"""
    Visões e suas Rotas...
"""

import logging
from flask import render_template, make_response
from flask.ext.babel import lazy_gettext as _
from flask.ext.appbuilder import BaseView, expose, has_access, ModelView, MultipleView
from app import db, cli, appbuilder
from container import ContainerModelView
from image import ImageModelView
from node import NodeModelView
from service import ServiceModelView
# from dashboard import DashboardModelView

# Início Log
log = logging.getLogger(__name__)


# ~~ Controlador de erro 404 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

appbuilder.base_template='orka/baselayout.html'
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Cria todas as tabelas de acordo com seus modelos
db.create_all()


# ~~ Itens do Menu ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

appbuilder.add_link("Index", label=_("Index"), href='/', icon='fa-home')


appbuilder.add_link("Dashboard", label=_('Dashboard'),
                     category="Services", icon="fa-tachometer",
                    category_icon='fa-server', href="/service/dashboard")

appbuilder.add_view(ServiceModelView, "Management", label=_("Management"),
                    category="Services", icon="fa-cubes")

appbuilder.add_view(NodeModelView, "Nodes", icon='fa-sitemap',
                    label=_('Nodes'), category="Services",
                    category_icon='fa-server', category_label=_('Services'))

appbuilder.add_view(ContainerModelView, "Container", label=_('Container'),
                    icon='fa-database')

appbuilder.add_view(ImageModelView, "Images", label=_('Images'),
                    icon='fa-hdd-o')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~ Permissões do Usuário ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
security = appbuilder.sm

active_views = [
    "Container",
    "Image",
    "Images",
    "Dashboard",
    "UserInfoEditView",
    "ResetPasswordView",
    "ResetMyPasswordView",
    "OrkaUserDBView",
    "Service",
    "Services"
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from config import APP_VERSION



log.info(10*" " + " ~~~~~~~~~~/---------- ORKA v{0} --------------\~~~~~~~~~~            ".format(APP_VERSION))

log.info(10*" " + " ~~~~~~~~~~\_______Flask APPBUILDER v{0}_______/~~~~~~~~~~            ".format(appbuilder.version))

