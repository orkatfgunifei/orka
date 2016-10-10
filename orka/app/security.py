from flask import redirect
from flask_appbuilder.security.views import UserDBModelView
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask.ext.appbuilder.actions import action
from flask.ext.appbuilder.security.registerviews import RegisterUserDBView
from flask.ext.babel import lazy_gettext as _


class OrkaUserDBView(UserDBModelView):
    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket", single=False)
    def muldelete(self, items):
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())


class RegisterUserDBView(RegisterUserDBView):
    email_template = 'security/register_mail.html'
    email_subject = _('Your Account activation')
    activation_template = 'activation.html'
    form_title = _('Fill out the registration form')
    error_message = _('Not possible to register you at the moment, try again later')
    message = _('Registration sent to your email')
    form_template = 'appbuilder/general/model/edit.html'


class OrkaSecurityManager(SecurityManager):
    userdbmodelview = OrkaUserDBView
    registeruserdbview = RegisterUserDBView

