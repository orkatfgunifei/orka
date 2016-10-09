#coding: utf-8

from . import BaseView, expose, has_access
from flask.ext.babel import lazy_gettext as _


class ImageView(BaseView):

    """
        A simple view that implements the index for the site
    """
    route_base = '/image'
    default_view = 'image'
    index_template = 'orka/image.html'

    base_permissions = ['can_edit', 'can_delete',
                        'can_download', 'can_list',
                        'can_add', 'can_show']

    @expose('/')
    def image(self):
        self.update_redirect()
        return self.render_template(self.index_template,
                                    appbuilder=self.appbuilder)
