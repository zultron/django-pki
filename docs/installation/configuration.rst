=============
Configuration
=============

Create and configure a new Django project
=========================================

If you don't have a django project yet create one now:

.. code-block:: bash
    
    $ django-admin.py startproject <YOUR_PROJECT_NAME>
    $ cd <YOUR_PROJECT_NAME>

Edit project's settings.py
==========================

1. Configure database (SQLite example):
    
  .. code-block:: python
        
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': '/Users/dkerwin/dev/dpki/pki.db', # Or path to database file if using sqlite3.
                'USER': '',                      # Not used with sqlite3.
                'PASSWORD': '',                  # Not used with sqlite3.
                'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            }
        }

2. Add django-pki template directory to TEMPLATE_DIRS if 'django.template.loaders.app_directories.Loader' is not in TEMPLATE_LOADERS:
    
  .. code-block:: python
        
        TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )

  **or**
  
  .. code-block:: python
        
        TEMPLATE_DIRS = ('/Library/Python/2.6/site-packages/pki/templates',)


3. Add 'pki.middleware.PkiExceptionMiddleware' to MIDDLEWARE_CLASSES (used for exception logging):
    
  .. code-block:: python
        
        MIDDLEWARE_CLASSES = (
            '...',
            'pki.middleware.PkiExceptionMiddleware',
        )

4. Add 'django.contrib.admin', 'south' and 'pki' to INSTALLED_APPS:

  .. warning:: Make sure **pki** is specified after **south** as unit tests won't work otherwise

  .. code-block:: python
        
        INSTALLED_APPS = (
            '...',
            'django.contrib.admin',
            'south',
            'pki',
        )

5. Set STATIC_URL and STATICFILES_DIRS

  If you are using Django version 1.4, then these settings are automatically handled by staticfiles.
  There is no need to make any changes to the settings.

5.1  If you are not using static files

  The values of STATIC_URL and STATICFILES_DIRS depend on your
  configuration.  STATICFILES_DIRS is the filesystem path to the
  django-pki static files (<PATH_TO_DJANGO_PKI>/media). You can of
  course copy or symlink the files to another location.  STATIC_URL is
  the URL part where the media files can be accessed.  Examples:

  .. code-block:: python

    STATICFILES_DIRS = '/Library/Python/2.6/site-packages/pki/media/'
    STATICFILES_DIRS = '/var/www/myhost/static/pki'
    
    STATIC_URL = '/static/'
    STATIC_URL = '/pki_media/'

5.2  Test

  Check that django can find the files from your project:

  ::

    python manage.py findstatic pki/js/pki_admin.js


6. Set ADMIN_MEDIA_PREFIX

Configure django-pki settings (in projects settings.py)
=======================================================

You can use any combination of the following parameters:

**PKI_DIR** (*Default = /path-to-django-pki/PKI; Type = Python String*)
    Absolute path to directory for pki storage. Must be writable

**PKI_OPENSSL_BIN** (*Default = /usr/bin/openssl; Type = Python String*)
    Path to openssl binary

**PKI_OPENSSL_CONF** (*Default = PKI_DIR/openssl.conf; Type = Python String*)
    Location of OpenSSL config file (openssl.conf)

**PKI_OPENSSL_TEMPLATE** (*Default = pki/openssl.conf.in; Type = Python String*)
    OpenSSL configuration template (Shouldn't be changen unless really neccessary)

**PKI_LOG** (*Default = PKI_DIR/pki.log; Type = Python String*)
    Full qualified path to logfile for PKI actions

**PKI_LOGLEVEL** (*Default = info; Type = Python String*)
    Logging level according to Python logging module

**JQUERY_URL** (*Default = pki/jquery-1.4.2.min.js; Type = Python String*)
    Alternative jQuery url

**PKI_SELF_SIGNED_SERIAL** (*Default = 0x0; Type = Python Number*)
    The serial of self-signed certificates. Set to 0 or 0x0 to get a random number (0xabc = HEX; 123 = DEC)

**PKI_DEFAULT_KEY_LENGTH** (*Default = 1024; Type = Python Number*)
    The default key length

**PKI_DEFAULT_COUNTRY** (*Default = DE; Type = Python String*)
    The default country (as 2-letter code) selected (http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

**PKI_DEFAULT_STATE** (*Default = ''; Type = Python String*)
    The default state or province name (full name)

**PKI_DEFAULT_LOCALITY** (*Default = ''; Type = Python String*)
    The default locality name (eg. city)

**PKI_DEFAULT_ORGANIZATION** (*Default = ''; Type = Python String*)
    The default organization name (eg. company)

**PKI_DEFAULT_OU** (*Default = ''; Type = Python String*)
    The default organizational unit name (eg. section)

**PKI_PASSPHRASE_MIN_LENGTH** (*Default = 8; Type = Python Number*)
    The minimum length for passphrases

**PKI_ENABLE_GRAPHVIZ** (*Default = False; Type = Python Boolean*)
    Enable graphviz support (see requirements)

**PKI_GRAPHVIZ_DIRECTION** (*Default = LR; Type = Python String*)
    Graph tree direction (LR=left-to-right, TD=top-down)

**PKI_ENABLE_EMAIL** (*Default = False; Type = Python Boolean*)
    Email delivery to certificate's email address. May require additional `Django paramters (EMAIL_*) <http://docs.djangoproject.com/en/dev/ref/settings/>`_

**Example:**
::
    
    ## django-pki specific parameters
    PKI_DIR = '/var/pki/ssl_store'
    PKI_OPENSSL_BIN = '/opt/openssl/bin/openssl'
    PKI_OPENSSL_CONF = '/opt/openssl/bin/etc/openssl.conf'
    PKI_LOG = '/var/log/django-pki.log'
    PKI_LOGLEVEL = 'error'
    JQUERY_URL = 'http://static.company.com/js/jquery.js'
    PKI_SELF_SIGNED_SERIAL = 0x0
    PKI_DEFAULT_KEY_LENGTH = 2048
    PKI_DEFAULT_COUNTRY = 'UK'
    PKI_PASSPHRASE_MIN_LENGTH = 12
    PKI_ENABLE_GRAPHVIZ = True
    PKI_GRAPHVIZ_DIRECTION = 'TD'
    PKI_ENABLE_EMAIL = True
    
    ## django specific email configuration
    EMAIL_HOST = "192.168.1.1"
    EMAIL_HOST_USER = "relayuser"
    EMAIL_HOST_PASSWORD = "icanrelay"
    DEFAULT_FROM_EMAIL = "pki@my-company.com"

Configure projects urls.py
==========================

1. Enable admin application::
    
    from django.contrib import admin 
    admin.autodiscover()

2. Add exception handler::
    
    handler500 = 'pki.views.show_exception'

3. Add the following lines to urlpatterns

  ::
    
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('pki.urls', 'pki')),

4. If you want to serve static files with ``./manage.py runserver`` in DEBUG mode, add the following code:
    
  .. warning:: **!! Do not use this in production !!**
    
  ::

    from django.conf import settings
    
    if settings.DEBUG:
        M = settings.MEDIA_URL
        if M.startswith('/'): M = M[1:]
        if not M.endswith('/'): M += '/'
        urlpatterns += patterns('', (r'^%s(?P<path>.*)$' % M, 'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT}))

Initialize database
===================

* Initialize database::
    
    $ python manage.py syncdb
    Syncing...
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table auth_message
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    Creating table south_migrationhistory
    
    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (Leave blank to use 'dkerwin'): admin
    E-mail address: a@b.com
    Password: 
    Password (again): 
    Superuser created successfully.
    Installing index for auth.Permission model
    Installing index for auth.Group_permissions model
    Installing index for auth.User_user_permissions model
    Installing index for auth.User_groups model
    Installing index for auth.Message model
    Installing index for admin.LogEntry model
    No fixtures found.
    
    Synced:
     > django.contrib.auth
     > django.contrib.contenttypes
     > django.contrib.sessions
     > django.contrib.sites
     > django.contrib.messages
     > django.contrib.admin
     > debug_toolbar
     > south
    
    Not synced (use migrations):
     - pki
    (use ./manage.py migrate to migrate these)

* Create django-pki tables. This is a south migration::
    
    $ python manage.py migrate pki
    Running migrations for pki:
     - Migrating forwards to 0003_auto__add_pkichangelog.
     > pki:0001_initial
     > pki:0002_auto__add_field_certificateauthority_crl_distribution
     > pki:0003_auto__add_pkichangelog
     - Loading initial data for pki.
    No fixtures found.


Initialize database
===================
Load fixtures
python manage.py loaddata pki/fixtures/eku_and_ku.json


PKI store layout (PKI_DIR)
==========================

Every certificate authority (CA) lives in a dedicated directory in PKI_DIR. There is a special directory named "_SELF_SIGNED_CERTIFICATES" which
contains all self-signed non-CA certificates. A certificate authority directory contains the follwoing sub-directories and files:

* Directories:
    * private: Private key of the CA
    * crl: Generated CRL
    * certs: All direct related certificates (subCA certificates or end-user certificates when it's a edge CA).
      Symlinks between the serialnumber and the hash are created for every certificate.
* Files:
    * index.txt(.old): The CA index
    * index.txt.attr(.old): Extra attribtes for index.txt
    * serial(.old): Current CA serial number
    * crlnumber(.old): Current CRL serial number
    * [CA NAME]-chain.cert.pem: The CA chain including the own CA certificate

Example::
    
    Root_CA/
    Root_CA/certs
    Root_CA/certs/01.pem
    Root_CA/certs/02.pem
    Root_CA/certs/518c671c.0
    Root_CA/certs/771a33d0.0
    Root_CA/certs/Root_CA.cert.pem
    Root_CA/crl
    Root_CA/crl/Root_CA.crl.pem
    Root_CA/crlnumber
    Root_CA/crlnumber.old
    Root_CA/index.txt
    Root_CA/index.txt.attr
    Root_CA/index.txt.attr.old
    Root_CA/index.txt.old
    Root_CA/private
    Root_CA/private/Root_CA.key.pem
    Root_CA/Root_CA-chain.cert.pem
    Root_CA/serial
    Root_CA/serial.old
    _SELF_SIGNED_CERTIFICATES/
    _SELF_SIGNED_CERTIFICATES/certs
    _SELF_SIGNED_CERTIFICATES/certs/selfsigned1.cert.pem
    _SELF_SIGNED_CERTIFICATES/certs/selfsigned1.key.pem

