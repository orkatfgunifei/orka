#coding: utf-8
from flask import jsonify
from flask.ext.babel import lazy_gettext as _
from . import BaseView, expose, has_access, make_response
from ..models.container import Container
from .. import db

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

    def str_to_dict(self, text):
        return eval(text)

    @expose('/')
    def container(self):
        self.update_redirect()

        #c = Container(name="One")
        #db.session.add(c)
        #db.session.commit()

        containers = db.session.query(Container).all()

        return self.render_template(self.index_template,
                                    appbuilder=self.appbuilder,
                                    container_ids=[c.id for c in containers]
                                    )

    @expose('/create')
    def create(self):
        return make_response("Vou criar jaja")