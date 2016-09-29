#coding: utf-8

from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from app.models.container import Container
from app import cli

class ContainerModelView(ModelView):

    datamodel = SQLAInterface(Container)

    list_columns = ['name',
                    'hostname',
                    'host',
                    'port',
                    'domain_name',
                    'cpu_reserved',
                    'storage_reserved',
                    'environment',
                    'image',
                    'node',
                    'container_type',
                    'docker_file']


    show_fieldsets = [
        ('Summary', {'fields': [
                        'name',
                        'domain_name',
                        'container_type'
                               ]}),
        (
            'Advanced Info',
            {'fields': [
                        'hostname',
                        'host',
                        'port',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved',
                        'environment',
                        'image',
                        'node',
                        'docker_file'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': [
                        'name',
                        'domain_name',
                        'container_type'
                               ]}),
        (
            'Advanced Info',
            {'fields': [
                        'hostname',
                        'host',
                        'port',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved',
                        'environment',
                        'image',
                        'node',
                        'docker_file'], 'expanded': True}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': [
                        'name',
                        'domain_name',
                        'container_type'
                               ]}),
        (
            'Advanced Info',
            {'fields': [
                        'hostname',
                        'host',
                        'port',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved',
                        'environment',
                        'image',
                        'node',
                        'docker_file'], 'expanded': False}),
    ]

    search_fieldsets = [
        ('Summary', {'fields': [
                        'name',
                        'domain_name',
                        'container_type'
                               ]}),
        (
            'Advanced Info',
            {'fields': [
                        'hostname',
                        'host',
                        'port',
                        'domain_name',
                        'cpu_reserved',
                        'storage_reserved',
                        'environment',
                        'image',
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

        if item.name:
            print item.name
