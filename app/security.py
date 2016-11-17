from flask.ext.appbuilder.widgets import ListThumbnail
from flask_appbuilder.security.views import UserDBModelView
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask.ext.appbuilder.security.registerviews import RegisterUserDBView
from flask.ext.babel import _ as _
from app.models.user import OrkaUser


class OrkaUserDBModelView(UserDBModelView):

    list_widget = ListThumbnail

    def __init__(self, **kwargs):
        super(OrkaUserDBModelView, self).__init__(**kwargs)

        photo_labels = {
            'photo_img': _('Logo'),
            'photo': _('Logo'),
            'photo_img_thumbnail': _('Logo'),
        }

        self.label_columns.update(photo_labels)

    show_fieldsets = [
        (_('User info'),
         {'fields': ['username', 'active', 'roles', 'login_count', 'photo_img']}),
        (_('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
        (_('Audit Info'),
         {'fields': ['last_login', 'fail_login_count', 'created_on',
                     'created_by', 'changed_on', 'changed_by'], 'expanded': False}),
    ]

    user_show_fieldsets = [
        (_('User info'),
         {'fields': ['username', 'active', 'roles', 'login_count', 'photo_img']}),
        (_('Personal Info'),
         {'fields': ['first_name', 'last_name', 'email'], 'expanded': True}),
    ]

    add_columns = ['first_name', 'last_name', 'username', 'active', 'email', 'roles', 'photo', 'password', 'conf_password']
    list_columns = ['first_name', 'last_name', 'username', 'email', 'active', 'roles', 'photo_img_thumbnail']
    edit_columns = ['first_name', 'last_name', 'username', 'active', 'email', 'roles', 'photo']


class RegisterUserDBView(RegisterUserDBView):

    email_template = 'security/register_mail.html'
    email_subject = _('Your Account activation')
    activation_template = 'activation.html'
    form_title = _('Fill out the registration form')
    error_message = _('Not possible to register you at the moment, try again later')
    message = _('Registration sent to your email')
    form_template = 'appbuilder/general/model/edit.html'


class OrkaSecurityManager(SecurityManager):
    user_model = OrkaUser
    userdbmodelview = OrkaUserDBModelView
    registeruserdbview = RegisterUserDBView

