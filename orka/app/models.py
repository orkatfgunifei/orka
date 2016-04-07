import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from flask.ext.appbuilder import Model
from flask.ext.babelpkg import lazy_gettext as _


class User(Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    username = Column(String(60), unique = True, nullable=False)
    email = Column(String(60), unique = True, nullable=False)
    personal_phone = Column(String(20))

    def __repr__(self):
        return self.name
    
class Node(Model):
    __tablename__ = "node"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    node_id = Column(String(32), unique = True, nullable=False)
    ip = Column(String(64), unique = True, nullable=True)
    port = Column(Integer, unique = True, nullable=False)
    
    def __repr__(self):
        return self.name

class Image(Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)    
    virtual_size = Column(Integer)
    
    def __repr__(self):
        return self.name
    
#class Container_enum(Enum):
#    storage = "Storage"
#    application = "Application"

class Container(Model):
    __tablename__ = "container"
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    container_id = Column(String(32), unique = True, nullable=False)
    port = Column(Integer, unique = True, nullable=False)
    host = Column(String(32), unique = True, nullable=False)
    hostname = Column(String(32), unique = True, nullable=False)
    domain_name = Column(String(32), unique = True, nullable=False)
    cpu_reserved = Column(Integer, unique = True, nullable=False)
    storage_reserved = Column(Integer, unique = True, nullable=False)
    environment = Column(String(164), unique = True, nullable=False)
    docker_file = Column(Text, nullable=True)
    image_id = Column(Integer, ForeignKey('image.id'))
    image = relationship("Image")
    node_id = Column(Integer, ForeignKey('node.id'))
    node = relationship("Node")
    #container_type = Column('Type', Enum(Container_enum))
    
    def __repr__(self):
        return self.name


    
    
    
