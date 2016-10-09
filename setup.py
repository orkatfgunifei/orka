#coding: utf-8

import os
from setuptools import setup

# Orka
# Diogo Matos, Felipe Barbosa e Rafael Lima
# Plataforma de Gerenciamento de Contêineres Docker

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "orka",
    version = "0.2.1",
    author = "TFG Orka Equipe",
    author_email = "rafael@orka.odoo.com, diogo@orka.odoo.com, felipe@orka.odoo.com",
    description = ("Plataforma de Gerenciamento de Contêineres Docker"),
    license = "MIT",
    keywords = "docker python flask",
    #url = "http://packages.python.org/orka",
    packages=['orka'],
    long_description=read('README.md'),
    scripts=['orka/run.py'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)