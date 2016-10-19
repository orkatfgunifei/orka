#coding: utf-8
from . import Model, Column, Integer, String

class Image(Model):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    digest = Column(String(256))
    name = Column(String(64), unique=True, nullable=False)
    version = Column(String(20), default='latest')

    def __repr__(self):
        return self.name
