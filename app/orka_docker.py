#coding: utf-8
from docker import Client
from io import BytesIO
import docker

from app.models.node import Node
from app.models.container import Container
from app.models.image import Image

from flask.ext.babel import lazy_gettext as _

# ~~ Instância do Cliente Docker ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cli = Client(base_url='unix://var/run/docker.sock')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def read_log(object_id, type, appbuilder):
    """
    Retorna o log de um Container ou
    Imagem
    :param hash_id: Hash de identificação
    :return: String com log
    """
    if object_id:
        if type == "container":
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

    if item.port:
        p = item.port.split(':')
        ports = [int(porta) for porta in p]

    if item.image.name:
        if not item.image.version:
            item.image.version = "latest"

        image = "%s:%s" % (item.image.name, item.image.version)
    else:
        image = False

    return cli.create_container(
        name=item.name or None,
        ports=ports or None,
        image=image or None
    )


def remove_container(hash_id):
    return cli.remove_container(hash_id)


def status_container(status, hash_id):
    if status:
        cli.start(hash_id)
    else:
        cli.stop(hash_id)


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


def create_service(item, appbuilder=False):

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
