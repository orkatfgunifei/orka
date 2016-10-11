#coding: utf-8
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.orm.attributes import get_history

from orka_modeview import OrkaModelView
from app.models.container import Container
from service import db, cli, _

class ContainerModelView(OrkaModelView):

    datamodel = SQLAInterface(Container)

    list_title = _("List Container")

    show_title = _("Show Container")

    add_title = _("Add Container")

    edit_title = _("Edit Container")

    label_columns = {'name': _('Name'),
                     'image': _('Image'),
                     'node': _('Node'),
                     'port': _('Port'),
                     'hash_id': _('ID Container'),
                     'domain_name': _('Domain Name'),
                     'cpu_reserved': _('CPU Reserved'),
                     'storage_reserved': _('Storage Reserved'),
                     'node': _('Node'),
                     'docker_file': _('Docker File'),
                     'status': _('Status')
                     }

    list_columns = ['name',
                    'image',
                    'node',
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
                        'storage_reserved',
                        'node',
                        'docker_file'], 'expanded': False}),
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
                        'storage_reserved',
                        'node',
                        'docker_file'], 'expanded': True}),
    ]

    edit_fieldsets = [
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
                        'storage_reserved',
                        'node',
                        'docker_file'], 'expanded': False}),
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
                        'storage_reserved',
                        'node',
                        'docker_file'], 'expanded': False}),
    ]

    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do container
        :param item: objeto Container definido em models
        :return:
        """
        super(ContainerModelView, self).pre_add(item)

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




