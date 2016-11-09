#coding: utf-8
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.models.mixins import ImageColumn
from flask import Markup, url_for

from app.models import (
    Column, Integer, ForeignKey, String,
    Sequence, Table, relationship, backref,
    Model, UserExtensionMixin)

class OrkaUser(User):

    photo = Column(ImageColumn(size=(300, 300, True), thumbnail_size=(150, 150, True)))

    def photo_url(self):
        im = ImageManager()

        if self.photo:
            return url_for('static', filename=im.get_url(self.photo)[8:])
        else:
            return im.get_url('avatar-default.png')

    def photo_img(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="' + url_for('OrkaUserDBModelView.show',pk=str(self.id)) +\
                '" class="thumbnail"><img src="' + im.get_url(self.photo) +\
                '" alt="Photo" class="profile-user-img img-responsive img-circle"></a>')
        else:
            return Markup(
                '<a href="' + url_for('OrkaUserDBModelView.show',pk=str(self.id)) +\
                '" class="thumbnail"><img src="' + im.get_url('avatar-default.png') +\
                '" alt="Photo" class="profile-user-img img-responsive img-circle"></a>')

    def photo_img_thumbnail(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="' + url_for('OrkaUserDBModelView.show',pk=str(self.id)) +\
                '" class="thumbnail"><img src="' + im.get_url_thumbnail(self.photo) +\
                '" alt="Photo" class="profile-user-img img-responsive img-circle"></a>')
        else:
            return Markup(
                '<a href="' + url_for('OrkaUserDBModelView.show',pk=str(self.id)) +\
                '" class="thumbnail"><img src="' + im.get_url_thumbnail('avatar-default.png') +\
                '" alt="Photo" class="profile-user-img img-responsive img-circle"></a>')
