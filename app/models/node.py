#coding: utf-8
from . import Model, Column, Integer, String


class Node(Model):

    __tablename__ = "node"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    remote_addr = Column(String(64))
    remote_port = Column(Integer)
    listen_addr = Column(String(64))
    listen_port = Column(Integer)
    join_token = Column(String(32))

    def __repr__(self):
        return self.name