#coding: utf-8
from app import db, appbuilder, cli
from app.views import _, BaseView, expose, has_access


class ServiceView(BaseView):

    """
        A simple view that implements the index for the site
    """
    route_base = '/service'
    default_view = 'service'
    index_template = 'orka/services.html'

    base_permissions = ['can_edit', 'can_delete',
                        'can_download', 'can_list',
                        'can_add', 'can_show']

    @expose('/')
    def service(self):
        self.update_redirect()
        return self.render_template(self.index_template,
                                    appbuilder=self.appbuilder)






