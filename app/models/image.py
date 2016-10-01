#coding: utf-8
from . import Model, Column, Integer, String

class Image(Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    virtual_size = Column(Integer)

    def __repr__(self):
        return  self.name