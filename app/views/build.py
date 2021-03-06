#coding: utf-8

from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from app.models.build import Build
from flask.ext.babel import lazy_gettext as _
from app.models.image import Image
from app.api.orka import build

class BuildModelView(ModelView):
    # TODO: Upload DockerFile
    datamodel = SQLAInterface(Build)

    route_base = "/build"

    base_order = ('name', 'asc')

    list_title = _("List Build")

    show_title = _("Show Build")

    add_title = _("Add Build")

    edit_title = _("Edit Build")

    label_columns = {'name': _('Name'),
                     'docker_file': _('Dockerfile')
                     }

    list_columns = ['name']

    show_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'docker_file']}),
    ]

    add_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'docker_file'
                               ]}),
    ]

    edit_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'docker_file']}),
    ]

    search_columns = ['name', 'docker_file']


    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação do build
        :param item: objeto Build definido em models
        :return:
        """
        super(BuildModelView, self).pre_add(item)

        if item.docker_file:

            response = build(item)

            if response:
                image_build = Image()
                image_build.name = item.name
                self.appbuilder.session.add(image_build)
                self.appbuilder.session.commit()





    def pre_delete(self, item):
        """
        Antes de remover o buildm do banco
        mata o processo e remove
        :param item: objeto Build
        :return:
        """
        super(BuildModelView, self).pre_delete(item)

