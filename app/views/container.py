#coding: utf-8
from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy.orm.attributes import get_history

from app import cli
from app.models.container import Container
from . import db


class ContainerModelView(ModelView):

    datamodel = SQLAInterface(Container)



    list_columns = ['name',
                    'image',
                    'node',
                    'port',
                    'status',
                    ]


    show_fieldsets = [
        ('Summary', {'fields': [
                        'name',
                        'image',
                        'port',
                        'status'
                               ]}),
        (
            'Advanced Info',
            {'fields': [
                        'hash_id',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved',
                        'node',
                        'docker_file'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': [
                        'name',
                        'image',
                        'port'
                               ]}),
        (
            'Advanced Info',
            {'fields': [
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved',
                        'node',
                        'docker_file'], 'expanded': True}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': [
                        'name',
                        'image',
                        'port',
                        'status'
                               ]}),
        (
            'Advanced Info',
            {'fields': [
                        'hash_id',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved',
                        'node',
                        'docker_file'], 'expanded': False}),
    ]

    search_fieldsets = [
        ('Summary', {'fields': [
                        'name',
                        'image',
                        'port',
                        'status'
                               ]}),
        (
            'Advanced Info',
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

        if item.name:
            resp = cli.run(item)
            if not resp[0] or "Error" in resp or "error" in resp:
                raise RuntimeError("Não foi possível criar o container [%s]" % (item.name))
            elif resp[0]:
                item.hash_id = resp[1]
                item.status = True



    def pre_delete(self, item):
        """
        Antes de remover o container do banco
        mata o processo e remove
        :param item: objeto Container
        :return:
        """
        super(ContainerModelView, self).pre_delete(item)

        if item.name:
            resp = cli.rm(item.name)

            if not resp:
                raise RuntimeError("Não foi possível remover o container [%s]" % (item.name))



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
            cli.rename(name.deleted[0], name.added[0])

        status = get_history(container, 'status')

        if not len(status.unchanged) > 0:
            if status.added[0]:
                cli.start(item.name)
            else:
                cli.stop(item.name)




