#coding: utf-8
from subprocess import Popen, PIPE
import json

"""
    API Docker - Python
    Orka
"""

class Docker():

    def run(self, name):
        """
        Executa uma imagem em um novo container
        Caso já exista ele retorna o nome do container
        :param name: Nome da imagem requisitada
        :return: (True ou False, hash_nome ou nome) --> Tupla de retorno
        """
        resp = self.execute('docker run -d ' + name)

        if resp != "":
            return  True, resp
        else:
            cmd = name.split().index('--name') + 1
            name = name.split()[cmd]
            print "[INFO] Container com nome: " + name + " já existente, modifique o nome.\n"
            return False, name


    def inspect(self, name):
        """
        Inspeciona um container
        :param name: nome do container
        :return: Retorna um dicionário com todas as informações do container
        """
        resp_json = self.execute('docker inspect ' + name)
        if resp_json:
            resp = json.loads(resp_json)[0]
            return resp
        else:
            return False

    def attach(self, name):
        # TODO: Criar Tratamento de threads !
        resp = self.execute('docker attach ' + name)
        print resp

    def rm(self, name):
        """
        Remoção de container
        :param name: nome ou hash do container
        :return: True se tudo ocorrer bem
        """
        return self.kill_and_remove(name)

    def start(self, name):
        """
        Inícia container
        :param name: nome do container
        :return: nome ou hash do container
        """
        return self.execute('docker start ' + name)

    def stop(self, name):
        """
        Encerra container
        :param name: nome do container
        :return: nome ou hash do container
        """
        return self.execute('docker stop ' + name)

    def list_containers(self, all=False):
        """
        Exibe no console a lista de containeres
        :param all: False para exibir apenas containeres ativos, e True para exibir todos
        :return: string com a lista de containeres
        """
        command = "docker ps"

        if all:
            command += " -a"

        return self.execute(command)

    def list_images(self):
        """
        Exibe as imagens na máquina
        :return: string com as informações das imagens disponíveis
        """
        return self.execute('docker images')

    def search(self, name):
        """
        Busca por imagens no Docker Hub
        :param name: Nome da imagem requisitada
        :return: retorna a lista dos containeres encontrados
        """
        return self.execute('docker search ' + name)

    def execute(self, command):
        """
        Executa comando dinamicamente
        :param parameters:
        :return: Saida da execução    """

        p = Popen(command.split(), stdout=PIPE)
        out = p.stdout.read()

        return out

    def top(self, name):
        """
        Exibe a lista dos principais processos em um container
        :param name: nome do container
        :return: string com a lista dos processos
        """
        return self.execute('docker top ' + name)

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

        return True


    def __repr__(self):
        return self.execute("docker version")


if __name__ == '__main__':
    a = Docker()
    print a
    comando = "-p 3000:3000 --name some-redmine redmine"
    imagem = a.run(comando)
    #print a.list_containers()


    #a.rm(imagem[1])

    #print a.inspect(imagem[1])

    #print a.search('odoo')

    #Necessário uso de thread para attach !
    # if imagem:
    #     a.attach(imagem[:8])
