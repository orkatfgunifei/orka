#coding: utf-8
from flask.ext.appbuilder.models.mixins import AuditMixin
from . import Model, Column, Integer,\
    String, relationship, Text, ForeignKey,\
    Boolean
from flask.ext.babel import lazy_gettext as _
from flask import Markup


class Container(AuditMixin, Model):

    __tablename__ = "container"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    hash_id = Column(String(256))
    ip = Column(String(16))
    port = Column(String(64))
    domain_name = Column(String(64))
    cpu_reserved = Column(Integer)
    storage_reserved = Column(Integer)
    image_id = Column(Integer, ForeignKey('image.id'))
    image = relationship("Image", lazy='subquery')
    status = Column(Boolean, default=False)
    type_id = Column(Integer, ForeignKey('containertype.id'))
    type = relationship("ContainerType")
    linked_id = Column(Integer, ForeignKey('container.id'), index=True)
    linked = relationship(lambda: Container, remote_side=id, backref='db_container')
    volumes = Column(String(256))
    environment = Column(String(256))
    command = Column(String(128))
    extra_params = Column(String(64))

    def port_match(self):

        if self.ip:

            if self.port:
                port = ""
                ports_list = self.port.split(',')
                ports = ports_list[0].split(':')

                if len (ports) == 2:
                    port = ports[1]
                elif len(ports) == 1:
                    port = ports[0]

                return port

    def ip_url_port(self):

        if self.ip:
            port = self.port_match()

            if port:
                return "%s:%s" % (self.ip, port)

            return "%s" % self.ip

    def ip_url(self):

        if self.ip:

            port = self.port_match()

            if port:
                return Markup(
                    '<a target="_blank" href="http://' + self.ip + ':' + port + '">' + self.ip + '</a>')
            else:
                return Markup(
                    '<a target="_blank" href="http://' + self.ip + '">' + self.ip + '</a>')
        else:
            return Markup(_('No IP'))

    def __repr__(self):
        return self.name


class ContainerType(Model):
    """
    Tipo de Container
    :atributo type: db, default
    """
    __tablename__ = "containertype"
    id = Column(Integer, primary_key=True)
    type = Column(String(32))

    types_i18n = {
        'default': _('Default'),
        'db': _('Database')
    }

    def __repr__(self):
        return str(self.types_i18n.get(str(self.type)))
