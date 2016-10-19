#coding: utf-8
from . import Model, Column, Integer, String


class Node(Model):

    __tablename__ = "node"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    listen_addr = Column(String(64), nullable=False, default="0.0.0.0")
    listen_port = Column(Integer, nullable=False, default=5000)
    advertise_addr = Column(String(64), nullable=False, default='127.0.0.1')
    remote_addr = Column(String(64))
    remote_port = Column(Integer)
    join_token = Column(String(32))
    snapshot_interval = Column(Integer, default=5000)
    log_entries_for_slow_followers = Column(Integer, default=1200)

    def __repr__(self):
        return self.name
