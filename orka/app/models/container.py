#coding: utf-8
from . import  Model, Column, Integer,\
    String, relationship, Text, ForeignKey, Boolean


class Container(Model):
    '''
        Definição container_type
        0: Storage
        1: Application
    '''
    __tablename__ = "container"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    hash_id = Column(String(64))
    port = Column(String(64))
    domain_name = Column(String(64))
    cpu_reserved = Column(Integer)
    storage_reserved = Column(Integer)
    docker_file = Column(Text)
    image_id = Column(Integer, ForeignKey('image.id'))
    image = relationship("Image")
    node_id = Column(Integer, ForeignKey('node.id'))
    node = relationship("Node")
    status = Column(Boolean, default=False)

    def __repr__(self):
        return self.name
