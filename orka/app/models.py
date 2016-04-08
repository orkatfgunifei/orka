#coding: utf-8
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Sequence
from sqlalchemy.orm import relationship, backref
from flask.ext.appbuilder import Model
from flask.ext.babelpkg import lazy_gettext as _
from flask_appbuilder.security.sqla.models import User



class OrkaUser(User):
    personal_phone = Column(String(20))

    
class Node(Model):
    __tablename__ = "node"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    node_id = Column(String(32), unique = True, nullable=False)
    ip = Column(String(64))

    
    def __repr__(self):
        return self.name

class Image(Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)    
    virtual_size = Column(Integer)
    
    def __repr__(self):
        return self.name

class Container(Model):
    ''' 
        Definição container_type
        0: Storage 
        1: Application
    '''
    __tablename__ = "container"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    container_id = Column(String(32))
    host = Column(String(32), nullable=True)
    hostname = Column(String(32))
    domain_name = Column(String(32))
    cpu_reserved = Column(Integer)
    storage_reserved = Column(Integer, nullable=True)
    environment = Column(String(164), nullable=True)
    docker_file = Column(Text, nullable=True)
    image_id = Column(Integer, ForeignKey('image.id'), nullable=True)
    image = relationship("Image")
    node_id = Column(Integer, ForeignKey('node.id'), nullable=True)
    node = relationship("Node")
    container_type = Column(Integer)
    
    def __repr__(self):
        return self.name


    
    
    
