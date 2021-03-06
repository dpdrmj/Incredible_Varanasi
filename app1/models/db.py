if not request.env.web2py_runtime_gae:
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('email', length=128, default='', unique=True), # required
    Field('password', 'password', length=512,            # required
          readable=False, label='Password'),
    #Field('address'),
    #Field('city'),
    #Field('zip'),
    #Field('phone'),
    Field('registration_key', length=512,                # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,              # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                 # required
          writable=False, readable=False, default=''))

## do not forget validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires =   [IS_NOT_EMPTY(error_message=auth.messages.is_empty),IS_ALPHANUMERIC(error_message='Not Alphanumeric')]
custom_auth_table.last_name.requires =   [IS_NOT_EMPTY(error_message=auth.messages.is_empty),IS_ALPHANUMERIC(error_message='Not Alphanumeric')]
custom_auth_table.password.requires =  [IS_STRONG(), CRYPT()]#CRYPT()#
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table


service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server ='smtp.gmail.com:587'
mail.settings.sender = 'deepakstudent8112@gmail.com'
mail.settings.login = 'deepakstudent8112:deepakstudent'

## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.messages.verify_email = 'Please click on the link http://' +     request.env.http_host +     URL(r=request,c='default',f='user',args=['verify_email']) +     '/%(key)s to verify your email'
auth.messages.reset_password = 'Please click on the link http://' +     request.env.http_host +     URL(r=request,c='default',f='user',args=['reset_password']) +     '/%(key)s to reset your password'



## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import RPXAccount
from gluon.contrib.login_methods.extended_login_form import ExtendedLoginForm
# The line below should be removed or commented
# auth.settings.actions_disabled=['register','change_password','request_reset_password']

# define where to go after RPX login
if request.vars._next:
    url = "http://127.0.0.1:8000/app1/default/user/login?_next=%s" % request.vars._next
else:
    url = "http://127.0.0.1:8000/app1/default/user/login"
rpxform = RPXAccount(request,
    api_key='59b03e232b8635f02aa670fd9e804d44dcf025f3',
    domain='incrediblevaranasi',
    url = "http://127.0.0.1:8000/app1/default/user/login")


from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')
