#coding: utf-8
from app import db
from app.models.service import Service
from app.views import BaseView, expose


class ServiceView(BaseView):

    """
        A simple view that implements the index for the site
    """
    route_base = '/service'
    default_view = 'service'

    base_template = 'orka/service/base.html'

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
        return self.render_template('orka/service/create.html',
                                    appbuilder=self.appbuilder,
                                    )






