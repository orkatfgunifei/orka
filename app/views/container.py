#coding: utf-8
from flask import g, redirect, url_for, request
from flask.ext.appbuilder import ModelView, expose, has_access
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.orm.attributes import get_history

from app import db, cli
from app.models.container import Container
from flask.ext.babel import lazy_gettext as _


class ContainerModelView(ModelView):

    datamodel = SQLAInterface(Container)
    route_base = '/container'
    default_view = 'container'

    @expose('/dashboard')
    @has_access
    def container(self):

        self.update_redirect()

        containers = db.session.query(Container).all()

        for container in containers:

            try:

                info_container = cli.inspect_container(container.hash_id)

                status = info_container.get('State')

                if not status['Running'] and container.status:
                    #containers.pop(index_container)
                    container.status = False
                elif status['Running'] and not container.status:
                    container.status = True

            except:
                container.status = False

        if db.session.dirty:
            db.session.commit()

        if not len(containers) > 0:
            return redirect(url_for('ContainerModelView.add'))

        return self.render_template('orka/container/base.html',
                                    appbuilder=self.appbuilder,
                                    containers=containers
                                    )

    list_title = _("List Container")

    show_title = _("Show Container")

    add_title = _("Add Container")

    edit_title = _("Edit Container")

    label_columns = {'name': _('Name'),
                     'image': _('Image'),
                     'port': _('Port'),
                     'hash_id': _('ID Container'),
                     'domain_name': _('Domain Name'),
                     'cpu_reserved': _('CPU Reserved'),
                     'storage_reserved': _('Storage Reserved'),
                     'status': _('Status')
                     }

    list_columns = ['name',
                    'image',
                    'port',
                    'status',
                    ]


    show_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'image',
                        'port',
                        'status'
                               ]}),
        (
            _('Advanced Info'),
            {'fields': [
                        'hash_id',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved'], 'expanded': False}),
    ]

    add_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'image',
                        'port'
                               ]}),
        (
            _('Advanced Info'),
            {'fields': [
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved'], 'expanded': True}),
    ]

    edit_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'image',
                        'port',
                        'status']}),
        (
            _('Advanced Info'),
            {'fields': [
                        'hash_id',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved'], 'expanded': False}),
    ]

    search_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'image',
                        'port',
                        'status'
                               ]}),
        (
            _('Advanced Info'),
            {'fields': [
                        'hash_id',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved'], 'expanded': False}),
    ]

    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do container
        :param item: objeto Container definido em models
        :return:
        """
        super(ContainerModelView, self).pre_add(item)

        if g.user.is_authenticated():
            item.user_id = g.user.id

            ports = []

            if item.port:
                p = item.port.split(':')
                ports = [int(porta) for porta in p]

            if item.image.name:
                if not item.image.version:
                    item.image.version = "latest"

                image = "%s:%s" % (item.image.name, item.image.version)
            else:
                image = False


            container = cli.create_container(
                name= item.name or None,
                ports= ports or None,
                image= image or None
                )

            if not container.get('Id'):
                raise RuntimeError("Não foi possível criar o container [%s]" % (item.name))
            else:

                item.hash_id = container.get('Id')
                #TODO: Checar size do container
                #cs = cli.inspect_container(item.hash_id)
                cli.start(item.hash_id)
                item.status = True



    def pre_delete(self, item):
        """
        Antes de remover o container do banco
        mata o processo e remove
        :param item: objeto Container
        :return:
        """
        super(ContainerModelView, self).pre_delete(item)

        if item.hash_id:
            cli.stop(item.hash_id)
            cli.remove_container(item.hash_id)


    def pre_update(self, item):
        """
        Antes de atualizar o container no banco
        renomeia o container e altera as demais modificações
        :param item: objeto Container
        :return:
        """
        super(ContainerModelView, self).pre_update(item)
        #len(old_name.unchanged)
        container = db.session.query(Container).get(item.id)

        # Verfica cada parâmetro por mudanças
        name = get_history(container, 'name')

        if not len(name.unchanged) > 0:
            cli.rename(item.hash_id, name.added[0])


        status = get_history(container, 'status')

        if not len(status.unchanged) > 0:
            if status.added[0]:
                cli.start(item.hash_id)

            else:
                cli.stop(item.hash_id)



