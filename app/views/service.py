#coding: utf-8
from app import db, appbuilder, cli
from app.views import _, BaseView, expose, has_access
from app.models.container import Container

class ServiceView(BaseView):

    """
        A simple view that implements the index for the site
    """
    route_base = '/services'
    default_view = 'services'
    index_template = 'orka/services.html'
    base_template = 'orka/services.html'
    base_permissions = ['can_edit', 'can_delete',
                        'can_download', 'can_list',
                        'can_add', 'can_show']

    @expose('/')
    def services(self):
        self.update_redirect()

        containers = db.session.query(Container).all()

        return self.render_template(self.base_template,
                                    appbuilder=self.appbuilder,
                                    containers=containers
                                    )






