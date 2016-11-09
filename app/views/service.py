#coding: utf-8
from app.models.service import Service
from app.models.node import Node
from app.views import expose, ModelView, has_access
from flask.ext.babel import lazy_gettext as _
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
#from sqlalchemy.orm.attributes import get_history
from app.api.orka import (
    create_service, remove_service, inspect_service, create_node
)
from flask import redirect, url_for, flash
import docker


class ServiceModelView(ModelView):

    datamodel = SQLAInterface(Service)

    route_base = "/service"

    list_title = _("List Service")

    show_title = _("Show Service")

    add_title = _("Add Service")

    edit_title = _("Edit Service")

    label_columns = {'name': _('Name'),
                     'image': _('Image'),
                     'node': _('Node'),
                     'command': _('Command'),
                     'status': _('Status'),
                     'service_id': _('ID Service')
                     }

    list_columns = [
                    'name',
                    'image',
                    'node',
                    'status',
                    ]

    show_fieldsets = [
        (_('Options'), {'fields': [
            'name',
            'image',
            'status',
        ]}),
        (_('Advanced'), {'fields': [
            'command',
            'node',
            'service_id'
        ], 'expanded': False})
    ]

    add_fieldsets = [
        (_('Options'), {'fields': [
            'name',
            'image',
        ]}),
        (_('Advanced'), {'fields': [
            'command',
            'node',
        ], 'expanded': True})
    ]

    edit_fieldsets = [
        (_('Options'), {'fields': [
            'name',
            'image',
            'status',
        ]}),
        (_('Advanced'), {'fields': [
            'command',
            'node',
            'service_id'
        ], 'expanded': False})
    ]

    search_columns = [
        'name',
        'image',
        'status',
        'command',
        'node',
        'service_id'
    ]

    @expose('/dashboard')
    @has_access
    def service(self):

        self.update_redirect()

        services = self.appbuilder.session.query(Service).all()

        for service in services:

            try:
                info_service = inspect_service(service.service_id)

                if info_service and not service.status:
                    service.status = True
            except:
                service.status = False

        if self.appbuilder.session.dirty:
            self.appbuilder.session.commit()

        if not len(services) > 0:
            return redirect(url_for('ServiceModelView.add'))

        return self.render_template('orka/service/base.html',
                                    appbuilder=self.appbuilder,
                                        services=services
                                        )

    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do serviço
        :param item: objeto Serviço definido em models
        :return:
        """
        item = create_service(item)
        super(ServiceModelView, self).pre_add(item)


    def pre_delete(self, item):
        """
        Antes de remover o serviço do banco
        :param item: objeto Serviço
        :return:
        """
        super(ServiceModelView, self).pre_delete(item)

        try:
            remove_service(item.name)
        except:
            print "Registro não encontrado, porém será removido"








