#coding: utf-8
from subprocess import Popen, PIPE


"""
    API Docker - Python
    Orka
"""

class Docker():

    def run(self, name):
        self.execute('docker run ' + name)

    def rm(self, name):
        self.kill_and_remove(name)

    def start(self, name):
        self.execute('docker start ' + name)

    def stop(self, name):
        self.execute('docker stop ' + name)

    def list(self, all=False):
        command = "docker ps"

        if all:
            command += " -a"

        self.execute(command)


    def execute(self, command):
        """
        Executa comando dinamicamente
        :param parameters:
        :return: Saida da execução    """

        p = Popen(command.split(), stdout=PIPE)
        out = p.stdout.read()

        return out

    def kill_and_remove(self, name):
        """
        Mata o processo do container e remove-o
        :param name:
        :return:
        """
        for action in ('kill', 'rm'):
            p = Popen('docker %s %s' % (action, name), shell=True,
                      stdout=PIPE, stderr=PIPE)
            if p.wait() != 0:
                raise RuntimeError(p.stderr.read())


    def __repr__(self):
        return self.execute("docker ps -a")


if __name__ == '__main__':
    a = Docker()
    print a
