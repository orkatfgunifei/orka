#coding: utf-8
import requests
from flask.ext.babel import lazy_gettext as _
from config import APP_VERSION

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

    def __init__(self, url, name):
        self.url = url
        self.name = name


def get_current_url(current_request):

    if current_request and current_request.url_rule:
        route_url = current_request.host_url
        route_list = []

        if not current_request.url_rule.rule == '/':
            url_list = [x for x in current_request.url_rule.rule.split('/') if x]

            try:
                for route in url_list:

                    route_url += route
                    if url_list.index(route) < (len(url_list)-1):
                        route_url += '/'

                    r = requests.get(route_url)
                    status = r.status_code

                    if route:

                        route_name = route_labels.get(route)

                        if not route_name:
                            route_name = route.capitalize()
                        else:
                            route_name = route_name.capitalize()

                        if status in [404, 400]:
                            base = RouteBase(
                                url="#",
                                name=route_name)
                        else:
                            base = RouteBase(
                                url=route_url,
                                name=route_name)

                        route_list.append(base)

                return route_list
            except:
                return []
        else:
            return []
    else:
        return []


def get_app_version():
    return APP_VERSION
