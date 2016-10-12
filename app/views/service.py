#coding: utf-8
from app import db, appbuilder, cli
from app.views import _, BaseView, expose, has_access
from app.models.service import Service

class ServiceView(BaseView):

    """
        A simple view that implements the index for the site
    """
    route_base = '/service'
    default_view = 'service'
    index_template = 'orka/service.html'
    base_template = 'orka/service.html'
    base_permissions = ['can_edit', 'can_delete',
                        'can_download', 'can_list',
                        'can_add', 'can_show']

    @expose('/')
    def service(self):
        self.update_redirect()

        services = db.session.query(Service).all()

        return self.render_template(self.base_template,
                                    appbuilder=self.appbuilder,
                                    services=services
                                    )

    @expose('/create')
    def create(self):

        print "aeeeeeeee"
        return self.render_template(self.base_template,
                                    appbuilder=self.appbuilder,
                                    )






