#coding: utf-8
from . import Model, Column, Integer, String

class Node(Model):
    __tablename__ = "node"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    node_id = Column(String(256))
    ip = Column(String(64))
    network_config = Column(String(256))

    def __repr__(self):
        return self.name