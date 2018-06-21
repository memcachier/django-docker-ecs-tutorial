import os
import requests

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uzm+$u0x!7cylg$o@ma2%h$*0e2agwy^9+wxmrc00+&+tvnf4n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# To run on ECS, we need to set up Django's ALLOWED_HOSTS variable
# correctly.  There are two parts to this.
#
#  - First, we allow access under any ".elb.amazonaws.com" DNS name.
#    This isn't very secure, but is good enough for our purposes here.
#    In a real production environment, you would have a "real" DNS
#    CNAME record pointing at the load balancer, and would put this
#    into ALLOWED_HOSTS instead of the ELB wildcard.
#
#  - Second, we need to do a little trick to allow AWS's Elastic Load
#    Balancer health checking to connect.  These connections use the
#    IP address of the EC2 instance hosting our application, so we
#    need to get that information somehow.  The instances used to
#    support ECS Fargate run a container management agent that
#    provides metadata information as JSON data accessible via HTTP at
#    http://169.254.170.2 [1], so we use that.
#
# If a request to the task metadata endpoint works, then we're running
# ECS and set things up appropriately.  If not, we leave ALLOWED_HOSTS
# empty, since we're running locally in development mode.
#
# [1]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-metadata-endpoint.html

ALLOWED_HOSTS = []
try:
    metadata = requests.get('http://169.254.170.2/v2/metadata',
                            timeout=0.1).json()
    ip = metadata['Containers'][0]['Networks'][0]['IPv4Addresses'][0]
    ALLOWED_HOSTS = ['.elb.amazonaws.com', ip]
except requests.exceptions.ConnectionError:
    pass
del requests

# Application definition
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'main'
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'thumbnailer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'thumbnailer.wsgi.application'
