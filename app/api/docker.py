#coding: utf-8
import json
from subprocess import Popen, PIPE

"""
    API Docker - Python
    Orka
"""

class Docker():



    def info(self):
        return self.execute('docker info')

    def run(self, item):
        """
        Executa uma imagem em um novo container
        Caso já exista ele retorna o nome do container
        :param item: objeto Container
        :return: (True ou False, hash_nome ou nome) --> Tupla de retorno -p 3000:3000 --name some-redmine redmine
        """
        command = 'docker run -d '


        if item.port:
            command += "-p %s:%s " %(item.port, item.port)
        if item.name and item.image:
            command += "--name %s %s" %(item.name, item.image.name)

        resp = self.execute(command)


        if resp != "":
            return  True, resp
        else:
            return False, resp


    def inspect(self, name):
        """
        Inspeciona um container
        :param name: nome do container
        :return: Retorna um dicionário com todas as informações do container
        """
        resp_json = self.execute('docker inspect %s' % (name))
        if resp_json:
            resp = json.loads(resp_json)[0]
            return resp
        else:
            return False

    def attach(self, name):
        # TODO: Criar Tratamento de threads !
        resp = self.execute('docker attach %s' % (name))
        print resp

    def logs(self, name):
        """
        Recebe a saída do console de um container
        :param name: nome do container
        :return: string com o log se houver
        """

        log = self.execute('docker logs %s' % (name))

        if log:
            return log
        else:
            return False

    def push(self, name):
        """
        Envia uma imagem ou um repositório para o registro (Docker Hub)
        :param name: nome ou hash na imagem
        :return:
        """
        self.execute('docker push %s' % (name))


    def pull(self, name):
        """
        Recebe uma imagem ou repositório do registro (Docker Hub)
        :param name: nome ou hash da imagem
        :return:
        """
        self.execute(('docker pull %s' % (name)))

    def rm(self, name):
        """
        Remoção de container
        :param name: nome ou hash do container
        :return: True se tudo ocorrer bem
        """
        return self.kill_and_remove(name)

    def rmi(self, name):
        """
        Remoção de imagem
        :param name: nome da imagem
        :return:
        """
        return self.execute("docker rmi %s" % (name))

    def start(self, name):
        """
        Inícia container
        :param name: nome do container
        :return: nome ou hash do container
        """
        return self.execute('docker start %s' % (name))

    def stop(self, name):
        """
        Encerra container
        :param name: nome do container
        :return: nome ou hash do container
        """
        return self.execute('docker stop %s' % (name))

    def restart(self, name):
        """
        Reinicia um container
        :param name: nome do container
        :return: retorna o nome do container reiniciado
        """
        return self.execute('docker restart %s' % (name))

    def port(self, name):
        """
        Lista o mapeamento de portas de um container
        :param name: nome do container
        :return: string com as portas
        """
        return self.execute('docker port %s' % (name))


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
        return self.execute('docker search %s' % (name))

    def execute(self, command):
        """
        Executa comando dinamicamente
        :param command: String com o comando a ser executado
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
        return self.execute('docker top %s' % (name))


    def rename(self, name, new_name):
        """
        Renomeia o container
        :param name: nome do container
        :param new_name: novo nome do container
        :return: True se tudo ocorrer bem
        """
        self.execute('docker rename %s %s' % (name, new_name))
        return True

    def kill_and_remove(self, name):
        """
        Mata o processo do container e remove-o
        :param name:
        :return:
        """
        for action in ('kill', 'rm'):
            if action == 'kill':
                try:
                    p = Popen('docker %s %s' % (action, name), shell=True,
                      stdout=PIPE, stderr=PIPE)

                    if p.wait() != 0:
                        raise RuntimeError(p.stderr.read())
                except:
                    print "Não executando, apenas irá remover"
            else:
                p = Popen('docker %s %s' % (action, name), shell=True,
                          stdout=PIPE, stderr=PIPE)

                if p.wait() != 0:
                    raise RuntimeError(p.stderr.read())

        return True


    def __repr__(self):
        return "Docker API Urubu"


