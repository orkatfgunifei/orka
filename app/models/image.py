#coding: utf-8
from . import Model, Column, Integer, String
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.models.mixins import ImageColumn
from flask import Markup, url_for


class Image(Model):

    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    digest = Column(String(256))
    name = Column(String(64), unique=True, nullable=False)
    version = Column(String(20), default='latest')
    photo = Column(ImageColumn(size=(300, 300, True), thumbnail_size=(120, 120, True)))
    size = Column(String(128))

    def photo_url(self):
        im = ImageManager()

        if self.photo:
            return url_for('static', filename=im.get_url(self.photo)[8:])
        else:
            return im.get_url('image-default.png')

    def photo_img(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="' + url_for('ImageModelView.show',pk=str(self.id)) +\
                '" class="thumbnail"><img src="' + im.get_url(self.photo) +\
                '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup(
                '<a href="' + url_for('ImageModelView.show',pk=str(self.id)) +\
                '" class="thumbnail"><img src="' + im.get_url('image-default.png') +\
                '" alt="Photo" class="img-rounded img-responsive"></a>')

    def photo_img_thumbnail(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="' + url_for('ImageModelView.show',pk=str(self.id)) +\
                '" class="thumbnail"><img src="' + im.get_url_thumbnail(self.photo) +\
                '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup(
                '<a href="' + url_for('ImageModelView.show',pk=str(self.id)) +\
                '" class="thumbnail"><img src="' + im.get_url_thumbnail('image-default.png') +\
                '" alt="Photo" class="img-rounded img-responsive"></a>')

    def __repr__(self):
        return "%s:%s" % (self.name, self.version)
