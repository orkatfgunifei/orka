#coding: utf-8
from app.models.service import Service
from app.views import expose, ModelView, has_access
from flask.ext.babel import lazy_gettext as _
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
#from sqlalchemy.orm.attributes import get_history
from app.views import cli, db
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

    search_fieldsets = [
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

    @expose('/dashboard')
    @has_access
    def service(self):

        self.update_redirect()

        services = db.session.query(Service).all()

        for service in services:

            try:
                info_service = cli.inspect_service(service.service_id)

                if info_service and not service.status:
                    service.status = True
            except:
                service.status = False

        if db.session.dirty:
            db.session.commit()

        if not len(services) > 0:
            return redirect(url_for('ServiceModelView.add'))

        return self.render_template('orka/service/base.html',
                                    appbuilder=self.appbuilder,
                                        services=services
                                        )

    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do container
        :param item: objeto Container definido em models
        :return:
        """
        super(ServiceModelView, self).pre_add(item)

        if item.image:

            command = []
            if item.command:
                command = item.command.split()

            container_spec = docker.types.ContainerSpec(
                image=item.image.name, command=command
            )
            task_tmpl = docker.types.TaskTemplate(container_spec)

            try:
                service_id = cli.create_service(task_tmpl, name=item.name)

                if service_id:
                    item.service_id = service_id['ID']
                    item.status = True
            except Exception as e:
                if "docker swarm init" in str(e):
                    raise Exception(_("Please create the node first."))
                else:
                    raise e
        else:
            raise Exception(_("Please select an image to create the service."))

    def pre_delete(self, item):
        """
        Antes de remover o container do banco
        mata o processo e remove
        :param item: objeto Container
        :return:
        """
        super(ServiceModelView, self).pre_delete(item)

        try:
            cli.remove_service(item.name)
        except:
            print "Registro não encontrado, porém será removido"

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






