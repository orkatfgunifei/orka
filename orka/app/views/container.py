#coding: utf-8

from flask.ext.babel import lazy_gettext as _
from . import BaseView, expose, has_access


class ContainerView(BaseView):

    """
        A simple view that implements the index for the site
    """
    route_base = '/container'
    default_view = 'container'
    index_template = 'orka/container.html'

    base_permissions = ['can_edit', 'can_delete',
                        'can_download', 'can_list',
                        'can_add', 'can_show']

    @expose('/')
    def container(self):
        self.update_redirect()
        return self.render_template(self.index_template,
                                    appbuilder=self.appbuilder)
