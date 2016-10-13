#coding: utf-8


class RouteBase(object):

    def __init__(self, url, name, index):
        self.url = url
        self.name = name
        self.index = index


def get_current_url(request):

    route_list = []
    index = 0

    for route in request.url_rule.rule.split('/'):
        if route:
            route_list.append(
                RouteBase(
                    url=route,
                    name=route.capitalize(),
                    index=index)
            )
            index += 1

    return route_list
