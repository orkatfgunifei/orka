#coding: utf-8

import os
from setuptools import setup, find_packages

# Orka
# Diogo Matos, Felipe Barbosa e Rafael Lima
# Plataforma de Gerenciamento de Contêineres Docker


# Parser dos pacotes necessários
with open('requirements.txt') as f:
    reqs = f.read().splitlines()

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
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    install_requires=reqs,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points = {
                       'console_scripts': [
                           'orka = orka.__main__:main'
                       ]
                   },
)
