#coding: utf-8
from . import Model, Column, Integer, String

class Node(Model):
    __tablename__ = "node"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    node_id = Column(String(32), unique=True, nullable=False)
    ip = Column(String(64))

    def __repr__(self):
        return self.name