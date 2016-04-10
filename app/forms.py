
from wtforms import Form, StringField, Label
from wtforms.validators import DataRequired
from flask.ext.appbuilder.fieldwidgets import BS3TextFieldWidget, BS3TextAreaFieldWidget
from flask.ext.appbuilder.forms import DynamicForm


class Terminal(DynamicForm):
    bash = StringField(('Bash'),
        widget=BS3TextAreaFieldWidget())
    comando = StringField(('>'),
        validators = [DataRequired()],
        widget=BS3TextFieldWidget())
