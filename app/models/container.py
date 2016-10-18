#coding: utf-8
from flask.ext.appbuilder.models.mixins import AuditMixin
from . import Model, Column, Integer,\
    String, relationship, Text, ForeignKey, Boolean


class Container(AuditMixin, Model):

    __tablename__ = "container"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    hash_id = Column(String(64))
    ip = Column(String(16))
    port = Column(String(64))
    domain_name = Column(String(64))
    cpu_reserved = Column(Integer)
    storage_reserved = Column(Integer)
    image_id = Column(Integer, ForeignKey('image.id'))
    image = relationship("Image")
    status = Column(Boolean, default=False)

    def __repr__(self):
        return self.name
