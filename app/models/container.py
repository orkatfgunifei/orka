#coding: utf-8
from . import Model, Column, Integer,\
    String, relationship, Text, ForeignKey


class Container(Model):
    '''
        Definição container_type
        0: Storage
        1: Application
    '''
    __tablename__ = "container"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    container_id = Column(String(32))
    host = Column(String(32))
    hostname = Column(String(32))
    domain_name = Column(String(32))
    cpu_reserved = Column(Integer)
    storage_reserved = Column(Integer)
    environment = Column(String(164))
    docker_file = Column(Text)
    image_id = Column(Integer, ForeignKey('image.id'))
    image = relationship("Image")
    node_id = Column(Integer, ForeignKey('node.id'))
    node = relationship("Node")
    container_type = Column(Integer)

    def __repr__(self):
        return self.name