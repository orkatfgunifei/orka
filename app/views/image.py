#coding: utf-8
from orka_modeview import OrkaModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from container import ContainerModelView
from service import cli, _
from app.models.image import Image
import json

class ImageModelView(OrkaModelView):
    datamodel = SQLAInterface(Image)

    related_views = [ContainerModelView]

    label_columns = {'name': _('Name'),
                     'version': _('Version'),
                     'digest': _('Digest')
                     }

    list_columns = ['name', 'version']

    show_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'version',
                        'digest'
                               ]}),
    ]

    add_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'version',
                               ]}),
    ]

    edit_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'version'
                               ]}),
    ]

    search_fieldsets = [
        (_('Summary'), {'fields': [
                        'name',
                        'version',
                        'digest'
                               ]}),
    ]

    base_order = ('name', 'asc')

    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação da imagem
        :param item: objeto Image definido em models
        :return:
        """
        super(ImageModelView, self).pre_add(item)

        if item.name:
            if not item.version:
                item.version = "latest"

            image_raw = cli.pull("%s:%s" % (item.name, item.version))
            image_raw = image_raw.replace("\r\n","|")
            image_raw = image_raw.split("|")

            for raw in image_raw:
                try:
                    raw = json.loads(raw)
                    status = raw['status']

                    if status[:6] == "Digest":
                        item.digest = status[15:]
                except:
                    continue



    def pre_delete(self, item):
        """
        Antes de remover o imagem do banco
        mata o processo e remove
        :param item: objeto Image
        :return:
        """
        super(ImageModelView, self).pre_delete(item)

        if item.name:
            try:
                resp = cli.remove_image("%s:%s" % (item.name, item.version))
                if resp:
                    print resp
            except Exception as inst:
                if inst.response.status_code == 409:
                    #TODO: Perguntar se deseja remover o container associado
                    print "Necessita remover container associado a imagem"


