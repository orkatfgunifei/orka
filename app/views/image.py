#coding: utf-8
import json
from flask.ext.appbuilder.widgets import ListThumbnail
from flask.ext.appbuilder import ModelView, expose, has_access
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from app.api.orka import image_pull, image_remove, list_images, create_object
from app.models.image import Image
from container import ContainerModelView, _
from service import ServiceModelView
from flask import redirect, url_for

class ImageModelView(ModelView):

    datamodel = SQLAInterface(Image)

    route_base = "/image"

    related_views = [ContainerModelView, ServiceModelView]

    list_widget = ListThumbnail

    list_title = _("List Image")

    show_title = _("Show Image")

    add_title = _("Add Image")

    edit_title = _("Edit Image")

    label_columns = {'name': _('Name'),
                     'version': _('Version'),
                     'digest': _('Digest'),
                     'photo': _('Logo'),
                     'photo_img_thumbnail': _('Logo'),
                     'photo_img': _('Logo'),
                     'size': _('Size')
                     }

    list_columns = ['name', 'version', 'size', 'photo_img_thumbnail']

    show_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'version',
                        'digest',
                        'size',
                        'photo_img'
                               ]}),
    ]

    add_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'version',
                        'photo'
                               ]}),
    ]

    edit_fieldsets = [
        (_('Options'), {'fields': [
                        'name',
                        'version',
                        'photo'
                               ]}),
    ]

    search_columns = ['name', 'version', 'digest']

    base_order = ('name', 'asc')


    @expose('/list/')
    @has_access
    def list(self):
        list_parent = super(ImageModelView, self).list()

        db_images = self.appbuilder.session.query(Image).all()

        host_images = list_images()

        in_host = False

        for db_image in db_images:

            for image in host_images:
                if image.get('IMAGE ID') and db_image.digest:
                    if image.get('IMAGE ID') in db_image.digest:
                        host_images.pop(host_images.index(image))
                        in_host = True
                        break

            if not in_host:
                self.appbuilder.session.delete(db_image)
                self.appbuilder.session.commit()

            in_host = False

        for image in host_images:
            if image.get('REPOSITORY'):
                objeto = {
                    'name': image.get('REPOSITORY'),
                    'digest': image.get('IMAGE ID') or None,
                    'size': image.get('SIZE') or None
                }

                if not ('<none>' in image.get('TAG')):
                    objeto['version'] = image.get('TAG')

                new_image = create_object("Image", objeto, self.appbuilder)

                if new_image:
                    db_images.append(new_image)

        if self.appbuilder.session.dirty:
            self.appbuilder.session.commit()

        if not len(db_images) > 0:
            return redirect(url_for('ImageModelView.add'))

        return list_parent

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

            image_raw = image_pull(item.name, item.version)
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
                resp = image_remove(item.name, item.version, item.digest)
                if resp:
                    print resp
            except Exception as inst:
                if inst.response.status_code == 409:
                    #TODO: Perguntar se deseja remover o container associado
                    print "Necessita remover container associado a imagem"



