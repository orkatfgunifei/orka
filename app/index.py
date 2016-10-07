from flask.ext.appbuilder.security.registerviews import RegisterUserDBView
from flask.ext.appbuilder import IndexView
from flask.ext.babelpkg import lazy_gettext as _


class IndexView(IndexView):
    index_template = 'index.html'


class RegisterUserDBView(RegisterUserDBView):
    email_template = 'security/register_mail.html'
    email_subject = _('Your Account activation')
    activation_template = 'activation.html'
    form_title = _('Fill out the registration form')
    error_message = _('Not possible to register you at the moment, try again later')
    message = _('Registration sent to your email')


