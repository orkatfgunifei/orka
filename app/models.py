#coding: utf-8
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Sequence, Date
from sqlalchemy.orm import relationship, backref
from flask.ext.appbuilder import Model
from flask.ext.babelpkg import lazy_gettext as _
from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.models.mixins import UserExtensionMixin

mindate = datetime.date(datetime.MINYEAR, 1, 1)


class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name

class UserExtended(Model, UserExtensionMixin):
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'), nullable=True)
    contact_group = relationship("ContactGroup")

class Contact(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique = True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'), nullable=False)
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey('gender.id'), nullable=False)
    gender = relationship("Gender")

    def __repr__(self):
        return self.name

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)

    
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
    name =  Column(String(150))
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


    
    
    
