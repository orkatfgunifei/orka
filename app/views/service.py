#coding: utf-8
from app.models.service import Service
from app.views import BaseView, expose, ModelView, MultipleView
from flask.ext.babel import lazy_gettext as _
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.orm.attributes import get_history
from container import cli, db
from flask import url_for, redirect
from app.views.node import NodeModelView

class ServiceModelView(ModelView):

    datamodel = SQLAInterface(Service)

    route_base = "/servicemodel"

    list_title = _("List Service")

    show_title = _("Show Service")

    add_title = _("Add Service")

    edit_title = _("Edit Service")


    label_columns = {'name': _('Name'),
                     'image': _('Image'),
                     'node': _('Node'),
                     'status': _('Status')
                     }

    list_columns = [
                    'name',
                    'image',
                    'node',
                    'status',
                    ]

    show_fieldsets = [
        (_('Summary'), {'fields': [
            'name',
            'image',
            'node',
            'status',
        ]})
    ]

    add_fieldsets = [
        (_('Summary'), {'fields': [
            'name',
            'image',
            'node',
        ]})
    ]

    edit_fieldsets = [
        (_('Summary'), {'fields': [
            'name',
            'image',
            'node',
            'status',
        ]})
    ]

    search_fieldsets = [
        (_('Summary'), {'fields': [
            'name',
            'image',
            'node',
            'status',
        ]})
    ]


    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do container
        :param item: objeto Container definido em models
        :return:
        """
        super(ServiceModelView, self).pre_add(item)

        # if g.user.is_authenticated():
        #     item.user_id = g.user.id
        #
        #     ports = []
        #
        #     if item.port:
        #         p = item.port.split(':')
        #         ports = [int(porta) for porta in p]
        #
        #     if item.image.name:
        #         if not item.image.version:
        #             item.image.version = "latest"
        #
        #         image = "%s:%s" % (item.image.name, item.image.version)
        #     else:
        #         image = False
        #
        #     container = cli.create_container(
        #         name=item.name or None,
        #         ports=ports or None,
        #         image=image or None
        #     )
        #
        #     if not container.get('Id'):
        #         raise RuntimeError("Não foi possível criar o container [%s]" % (item.name))
        #     else:
        #
        #         item.hash_id = container.get('Id')
        #         # TODO: Checar size do container
        #         # cs = cli.inspect_container(item.hash_id)
        #         cli.start(item.hash_id)
        #         item.status = True


    def pre_delete(self, item):
        """
        Antes de remover o container do banco
        mata o processo e remove
        :param item: objeto Container
        :return:
        """
        super(ServiceModelView, self).pre_delete(item)

        # if item.hash_id:
        #     cli.stop(item.hash_id)
        #     cli.remove_container(item.hash_id)


    def pre_update(self, item):
        """
        Antes de atualizar o container no banco
        renomeia o container e altera as demais modificações
        :param item: objeto Container
        :return:
        """
        super(ServiceModelView, self).pre_update(item)
        # len(old_name.unchanged)
        # container = db.session.query(Container).get(item.id)
        #
        # # Verfica cada parâmetro por mudanças
        # name = get_history(container, 'name')
        #
        # if not len(name.unchanged) > 0:
        #     cli.rename(item.hash_id, name.added[0])
        #
        # status = get_history(container, 'status')
        #
        # if not len(status.unchanged) > 0:
        #     if status.added[0]:
        #         cli.start(item.hash_id)
        #
        #     else:
        #         cli.stop(item.hash_id)


class ServiceView(MultipleView):

    """
        A simple view that implements the index for the site
    """
    views = [ServiceModelView, NodeModelView]
    route_base = '/service'
    #default_view = 'service'

    @expose('/list')
    def service(self):
        self.update_redirect()

        services = db.session.query(Service).all()

        return self.render_template('orka/service/base.html',
                                    appbuilder=self.appbuilder,
                                    services=services
                                    )






