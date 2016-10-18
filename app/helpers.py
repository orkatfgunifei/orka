#coding: utf-8
import requests

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

                url = current_request.base_url
                r = requests.get(url)
                status = r.status_code

                if status in [404, 400]:
                    url = False

                if route:
                    route_list.append(
                        RouteBase(
                            url=url or "#",
                            name=route.capitalize(),
                            index=index)
                    )
                    index += 1

            return route_list
        except:
            return []
    else:
        return []



