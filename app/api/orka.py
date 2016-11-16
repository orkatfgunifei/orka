#coding: utf-8
import re
from docker import Client
from io import BytesIO
import docker
from app.api.urubu import Urubu
from app.models.node import Node
from app.models.container import Container
from app.models.image import Image

from flask.ext.babel import lazy_gettext as _
from app.models.container import Container
from app.models.image import Image

# ~~ Instância do Cliente Docker ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cli = Client(base_url='unix://var/run/docker.sock')
urubu = Urubu()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def create_object(modelo, objeto_dict, appbuilder):

    if modelo == "Container":

        c = Container()

        if objeto_dict.get('name'):
            c.name = objeto_dict.get('name')

        if objeto_dict.get('hash_id'):
            c.hash_id = objeto_dict.get('hash_id')

        if objeto_dict.get('command'):
            c.command = objeto_dict.get('command')

        if objeto_dict.get('status'):
            c.status = objeto_dict.get('status')

        if objeto_dict.get('ip'):
            c.ip = objeto_dict.get('ip')

        if objeto_dict.get('image'):

            info = objeto_dict.get('image').split(':')

            images = []

            if len(info) == 2:
                images = appbuilder.session.query(Image).\
                    filter_by(name=info[0], version=info[1]).all()
            elif len(info) == 1:
                images = appbuilder.session.query(Image).\
                    filter_by(name=info[0]).all()

            if len(images) == 1:
                c.image_id = images[0].id
            else:
                new_image = Image()
                new_image.name = info[0]

                if len(info) == 2:
                    new_image.version = info[1]

                appbuilder.session.add(new_image)
                appbuilder.session.commit()
                c.image_id = new_image.id

        appbuilder.session.add(c)
        appbuilder.session.commit()

        return c



def read_log(object_id, log_type, appbuilder):
    """
        Retorna o log de um Container ou Imagem
    :param object_id: Hash de identificação
    :param log_type: Tipo do objeto container ou imagem
    :param appbuilder: objeto que contem session para uso do db
    :return:
    """
    if object_id:
        if log_type == "container":
            container = appbuilder.session.query(Container).get(int(object_id))
            hash_id = container.hash_id
            logs = cli.logs(hash_id)
            linhas = logs.split("- -")

            for linha in linhas:
                # Limpando ao máximo, uow
                linhas[linhas.index(linha)] = linha.replace('\"-\"', "").replace('\"', '')

            return linhas


def rename_container(old_name, new_name):
    return cli.rename(old_name, new_name)


def inspect_container(hash_id):
    return cli.inspect_container(hash_id)


def create_container(item):

    ports = []
    container = {}

    if not (item.linked or item.environment
            or item.volumes or item.command
            or item.extra_params):

        if item.port:
            p = item.port.split(':')
            ports = [int(porta) for porta in p]

        if item.image.name:
            if not item.image.version:
                item.image.version = "latest"
                image = "%s" % item.image.name
            elif item.image.version == "latest":
                image = "%s" % item.image.name
            else:
                image = "%s:%s" % (item.image.name, item.image.version)


        else:
            image = False

        container = cli.create_container(
            name=item.name or None,
            ports=ports or None,
            image=image or None
        )
    else:
        resp = urubu.run(item)

        if resp[0]:
            container = {'Id': resp[1].rstrip(), 'urubu': True}

    inspect = cli.inspect_container(container.get('Id'))

    if inspect['State']['Status'] == 'running':
        container.update({
            'running': True
        })

    if inspect.get('NetworkSettings'):
        ip_address = inspect['NetworkSettings']['Networks']['bridge']['IPAddress']

        container.update({
            'ip_address': ip_address
        })

    return container


def list_containers(list_all=False):

    host_containers = urubu.list_containers(list_all=list_all)

    row_splitter = re.compile("  +")  # Encontra uma sequência de dois ou mais espaços
    rows = host_containers.split('\n')  # Divide a tabela em uma lista de linhas

    headings = ['CONTAINER ID', 'IMAGE', 'COMMAND', 'CREATED', 'STATUS', 'PORTS', 'NAMES']
    headings_noport = ['CONTAINER ID', 'IMAGE', 'COMMAND', 'CREATED', 'STATUS', 'NAMES']

    # Cria uma lista de dicionários mapeando os valores
    template_dicts = []
    for row in rows:
        values = row_splitter.split(row)
        if len(values) == 6:
            head = headings_noport
        else:
            head = headings

        template_dict = dict(zip(head, values))
        template_dicts.append(template_dict)

    return template_dicts

def remove_container(hash_id):
    try:
        return cli.remove_container(hash_id)
    except:
        return "removed db only"


def status_container(status, hash_id):
    try:
        if status:
            cli.start(
                container=hash_id,
            )
        else:
            cli.stop(hash_id)
    except:
        print "container not exists"


def build(item):

    f = BytesIO(item.docker_file.encode('utf-8'))

    response = [line for line in cli.build(
        fileobj=f, rm=True,
        tag=item.name)]

    return response


def create_node(item):

    if item.listen_addr and item.advertise_addr:

        spec = cli.create_swarm_spec(
            snapshot_interval=item.snapshot_interval,
            log_entries_for_slow_followers=item.log_entries_for_slow_followers
        )
        listen_addr = '%s:%s' % (item.listen_addr, item.listen_port)

        try:
            resp = cli.init_swarm(
                advertise_addr=item.advertise_addr, listen_addr=listen_addr,
                force_new_cluster=False, swarm_spec=spec
            )
            print resp
        except Exception as e:
            message = str(e)

            if "docker swarm leave" in message:
                raise Exception(_("Node already initializated, use join instead."))
            elif "listen address must" in message:
                raise Exception(_("Please insert the listen IP address and Port, e.g  0.0.0.0:5000"))
            else:
                raise e


def remove_node(force=False):
    cli.leave_swarm(force=force)


def image_pull(name, version):
    return cli.pull("%s:%s" % (name, version))


def image_remove(name, version):
    return cli.remove_image("%s:%s" % (name, version))


def create_service(item):

    if item.image:

        command = []
        if item.command:
            command = item.command.split()

        container_spec = docker.types.ContainerSpec(
            image=item.image.name, command=command
        )
        task_tmpl = docker.types.TaskTemplate(container_spec)

        try:
            if not item.node:
                raise Exception(_("Please select a node for this service..."))

            service_id = cli.create_service(task_tmpl, name=item.name)

            if service_id:
                item.service_id = service_id['ID']
                item.status = True
                return item


        except Exception as e:
            if "docker swarm init" in str(e):
                # if appbuilder:
                #     node = Node()
                #
                #     node.name = "orka-node"
                #     node.listen_addr = "0.0.0.0"
                #     node.listen_port = 5000
                #     node.advertise_addr = '127.0.0.1'
                #
                #     create_node(node)
                #
                #     appbuilder.session.add(node)
                #
                #     appbuilder.session.commit()

                raise Exception(_("Please create the node first."))
            else:
                raise e
    else:
        raise Exception(_("Please select an image to create the service."))


def inspect_service(service_id):
    return cli.inspect_service(service_id)


def remove_service(name):
    cli.remove_service(name)
