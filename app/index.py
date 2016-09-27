from flask.ext.appbuilder.security.registerviews import RegisterUserDBView
from flask.ext.appbuilder import IndexView
from flask.ext.babelpkg import lazy_gettext as _
from flask_appbuilder import SimpleFormView
from flask.ext.appbuilder import expose, has_access
from flask import (
    flash, redirect, send_file, jsonify, make_response, url_for, session, abort)

from .bash import Bash

class IndexView(IndexView):
    index_template = 'index.html'


class RegisterUserDBView(RegisterUserDBView):
    email_template = 'security/register_mail.html'
    email_subject = _('Your Account activation')
    activation_template = 'activation.html'
    form_title = _('Fill out the registration form')
    error_message = _('Not possible to register you at the moment, try again later')
    message = _('Registration sent to your email')


class TerminalForm(SimpleFormView):

    def __init__(self, **kwargs):
        """
            Constructor
        """
        super(TerminalForm, self).__init__(**kwargs)
        self.bash = Bash()

    @expose("/form", methods=['POST'])
    @has_access
    def this_form_post(self):
        self._init_vars()
        form = self.form.refresh()

        #print form.validate_on_submit()


        form.bash.data = self.bash.send(form.comando.data)
        form.comando.data = ""

        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder
        )
