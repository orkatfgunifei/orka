#coding: utf-8
from subprocess import Popen, PIPE


def execute(*parameters):
    """
    Executa comando dinamicamente
    :param parameters:
    :return: Saida da execução    """

    p = Popen(parameters[0], stdout=PIPE)
    out = p.stdout.read()

    return out


def kill_and_remove(ctr_name):
    for action in ('kill', 'rm'):
        p = Popen('docker %s %s' % (action, ctr_name), shell=True,
                  stdout=PIPE, stderr=PIPE)
        if p.wait() != 0:
            raise RuntimeError(p.stderr.read())

#docker run --rm ubuntu:14.04 python3 -c "print('aee python333333')"

class Docker():

    def __repr__(self):
        parameters = ['docker', 'ps']
        ola = execute(parameters)
        return ola


a = Docker()
print a