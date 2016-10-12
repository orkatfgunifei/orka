#coding: utf-8
from flask.ext.appbuilder.models.mixins import AuditMixin
from . import Model, Column, Integer,\
    String, relationship, ForeignKey, Boolean


class Service(AuditMixin, Model):

    __tablename__ = "service"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    image_id = Column(Integer, ForeignKey('image.id'))
    image = relationship("Image")
    node_id = Column(Integer, ForeignKey('node.id'))
    node = relationship("Node")
    status = Column(Boolean, default=False)

    def __repr__(self):
        return self.name
