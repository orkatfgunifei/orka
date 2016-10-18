#coding: utf-8
import requests
from flask.ext.babel import lazy_gettext as _

black_list = ['usage']

route_labels = {
    'list': _('list'),
    'add': _('add'),
    'show': _('show'),
    'service': _('service'),
    'container': _('container'),
    'image': _('image'),
    'node': _('node'),
    'dashboard': _('dashboard'),
    'index': _('index'),
    'user': _('user'),
    'users': _('users'),
    'userinfo': _('userinfo'),
    'home': _('home')}

class RouteBase(object):

    def __init__(self, url, name, index):
        self.url = url
        self.name = name
        self.index = index


def get_current_url(current_request):
    if current_request:
        route_list = []
        index = 0

        try:
            for route in current_request.url_rule.rule.split('/'):

                if not route in black_list:
                    url = current_request.base_url
                    r = requests.get(url)
                    status = r.status_code

                    if status in [404, 400]:
                        url = False

                    if route:

                        route_name = route_labels.get(route)

                        if not route_name:
                            route_name = route.capitalize()
                        else:
                            route_name = route_name.capitalize()

                        route_list.append(
                            RouteBase(
                                url=url or "#",
                                name=route_name,
                                index=index)
                        )
                        index += 1

            return route_list
        except:
            return []
    else:
        return []



