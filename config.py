#coding: utf-8
import os
from flask_appbuilder.security.manager import AUTH_OID, AUTH_REMOTE_USER, AUTH_DB, AUTH_LDAP, AUTH_OAUTH
basedir = os.path.abspath(os.path.dirname(__file__))


# Modo de execução do servidor
RUN_MODE = ["PROD", "TEST", "DEV"][2]
# TODO: Se modo PROD utilizar postgresql, Se DEV ou TEST utilizar sqllite

# Your App secret key
SECRET_KEY = '\2\tfgunifeirules\1\2\e\y\y\h'

# The SQLAlchemy connection string.
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'
SQLALCHEMY_DATABASE_URI = 'postgresql://odoo:rmpa@localhost/orka'

# Flask-WTF flag for CSRF
CSRF_ENABLED = True

#------------------------------
# GLOBALS FOR APP Builder
#------------------------------
APP_NAME = "Orka"

APP_VERSION = "0.3.7"

if RUN_MODE != "PROD":
    APP_NAME += " [%s]" % RUN_MODE


# Uncomment to setup Setup an App icon
APP_ICON = "/static/img/logo.png"

#----------------------------------------------------
# AUTHENTICATION CONFIG
#----------------------------------------------------
# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database (username/password()
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
AUTH_TYPE = AUTH_DB

# Uncomment to setup Full admin role name
#AUTH_ROLE_ADMIN = 'Admin'

# Uncomment to setup Public role name, no authentication needed
#AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
AUTH_USER_REGISTRATION = True

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "User"

# When using LDAP Auth, setup the ldap server
#AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# Uncomment to setup OpenID providers example for OpenID authentication
#OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
#---------------------------------------------------
# Babel config for translations
#---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = 'pt_BR'
# Your application default translation path
BABEL_DEFAULT_FOLDER = 'translations'
# The allowed translation for you app
LANGUAGES = {
    'en': {'flag':'gb', 'name':'English'},
    'pt_BR': {'flag':'br', 'name': 'Pt Brazil'},
    'de': {'flag':'de', 'name':'German'},
}
#---------------------------------------------------
# Image and file configuration
#---------------------------------------------------
# The file upload folder, when using models with files
UPLOAD_FOLDER = basedir + '/app/static/uploads/'

# The image upload folder, when using models with images
IMG_UPLOAD_FOLDER = basedir + '/app/static/uploads/'

# The image upload url, when using models with images
IMG_UPLOAD_URL = '/static/uploads/'
# Setup image size default is (300, 200, True)
#IMG_SIZE = (300, 200, True)


# Config for Flask-WTF Recaptcha necessary for user registration
RECAPTCHA_PUBLIC_KEY = '6LedRP0SAAAAAOF03Nsv_ny2NzOF_Dthe_Xn269v'
RECAPTCHA_PRIVATE_KEY = '6LedRP0SAAAAAPnsdEKgj5VU1QbFcPv7mO8cW0So'

# Config for Flask-Mail necessary for user registration
MAIL_PORT=2525
MAIL_USE_SSL=False
MAIL_SERVER = 'mailtrap.io'
MAIL_USE_TLS = False
MAIL_USERNAME = '2cffba9d2d92fd'
MAIL_PASSWORD = '3cbdfc811f9313'
MAIL_DEFAULT_SENDER = 'rafael.liverpool@gmail.com'
#--------------------------------------

# Theme configuration
# these are located on static/appbuilder/css/themes
# you can create your own and easily use them placing them on the same dir structure to override
#APP_THEME = "bootstrap-theme.css"  # default bootstrap
APP_THEME = "styles.css"
