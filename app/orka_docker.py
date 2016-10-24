#coding: utf-8

from app import cli

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