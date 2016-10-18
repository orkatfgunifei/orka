#coding: utf-8
from . import Model, Column, Integer, String, Text


class Build(Model):

    __tablename__ = "build"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    docker_file = Column(Text, nullable=False,
             default="""
            # Example Dockerfile
            FROM busybox:buildroot-2014.02
            MAINTAINER first last, first.last@yourdomain.com
            VOLUME /data
            CMD ["/bin/sh"]
             """)

    def __repr__(self):
        return self.name
