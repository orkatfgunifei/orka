#coding: utf-8
from app.models.service import Service
from app.views import BaseView, expose, ModelView, MultipleView, has_access
from flask.ext.babel import lazy_gettext as _
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.orm.attributes import get_history
from container import cli, db
from flask import redirect, url_for, flash
import docker

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

    @expose('/')
    @has_access
    def service(self):
        print "passo aqui na rota de service"
        self.update_redirect()
        self.base_template = 'orka/service.html'
        services = db.session.query(Service).all()

        return self.render_template(self.base_template,
                                    appbuilder=self.appbuilder,
                                    service=services
                                    )


    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do container
        :param item: objeto Container definido em models
        :return:
        """
        super(ServiceModelView, self).pre_add(item)

        container_spec = docker.types.ContainerSpec(
            image='busybox', command=['echo', 'hello']
        )
        task_tmpl = docker.types.TaskTemplate(container_spec)
        service_id = cli.create_service(task_tmpl, name=item.name)

        if service_id:
            item.service_id = service_id['ID']



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


class ServiceView(BaseView):

    """
        A simple view that implements the index for the site
    """

    route_base = '/service'
    default_view = 'service'

    @expose('/service')
    def service(self):
        self.update_redirect()

        services = db.session.query(Service).all()

        return self.render_template('orka/service/base.html',
                                    appbuilder=self.appbuilder,
                                    services=services
                                    )






