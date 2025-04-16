import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-default-key-for-development'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'social_django',
    'portfolio',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'portfolio.middleware.Auth0SessionMiddleware',  # Add Auth0 session clearing middleware
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_for_pm',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

AUTH_USER_MODEL = 'portfolio.User'

# Auth0 Configuration
AUTH0_DOMAIN = 'dev-lrgbq7jwc8g46cow.us.auth0.com'
AUTH0_CLIENT_ID = 'r1u6ia6JhvGNoJA6bw52oylsNw40p2jm'
AUTH0_CLIENT_SECRET = 'lZ2pCeHzc9izvbfRF8QZpf1PU8dpqtVt0A2ReanWAUGenq8TsL6PNFXvjtrtsj4Z'

# Auth0 Logout Configuration
AUTH0_LOGOUT_URL = f'https://{AUTH0_DOMAIN}/v2/logout'
AUTH0_RETURN_TO_URL = 'http://127.0.0.1:8000'  # Your application's home page

SOCIAL_AUTH_AUTH0_DOMAIN = AUTH0_DOMAIN
SOCIAL_AUTH_AUTH0_KEY = AUTH0_CLIENT_ID
SOCIAL_AUTH_AUTH0_SECRET = AUTH0_CLIENT_SECRET

# Social Auth Configuration
SOCIAL_AUTH_TRAILING_SLASH = True  # Enable trailing slash
SOCIAL_AUTH_AUTH0_REDIRECT_URI = 'http://127.0.0.1:8000/complete/auth0/'

# OAuth2 settings
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email'
]

# Force Auth0 to always prompt for login and prevent caching
SOCIAL_AUTH_AUTH0_PARAMS = {
    'prompt': 'select_account consent',  # Added consent to force fresh login
    'max_age': 0,
    'connection_scope': 'offline_access',
    'response_mode': 'form_post',
    'response_type': 'code',
    'nonce': lambda: os.urandom(16).hex(),
}

# Prevent social auth from caching sessions
SOCIAL_AUTH_SESSION_EXPIRATION = True
SOCIAL_AUTH_CLEAN_USERNAMES = True
SOCIAL_AUTH_STORE_ACCESS_TOKEN = False
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = []
SOCIAL_AUTH_REMEMBER_SESSION_NAME = None
SOCIAL_AUTH_NO_DEFAULT_PROTECTED_USER_FIELDS = True

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'portfolio.auth0_backend.CustomAuth0OAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# JWT Settings
SOCIAL_AUTH_JWT_ENABLED = True
SOCIAL_AUTH_JWT_VERIFY = True
SOCIAL_AUTH_JWT_VERIFY_EXPIRATION = True
SOCIAL_AUTH_JWT_ALGORITHM = 'RS256'
SOCIAL_AUTH_JWT_DECODE_OPTIONS = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': False,
    'verify_aud': False,
    'verify_iss': False,
    'require_exp': False,
    'require_iat': False,
    'leeway': 0
}

# Additional JWT settings
SOCIAL_AUTH_JWT_LEEWAY = 300  # 5 minutes leeway
JWT_AUTH = {
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 600,  # 10 minutes
    'JWT_EXPIRATION_DELTA': timedelta(hours=24),
    'JWT_ALLOW_REFRESH': True,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

# Social Auth Pipeline
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Session Settings
SOCIAL_AUTH_SESSION_EXPIRATION = True
SESSION_COOKIE_SECURE = False  # Set to True in production
SESSION_COOKIE_HTTPONLY = True

# Allowed Hosts for Auth0
SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS = ['127.0.0.1:8000', 'localhost:8000']
SOCIAL_AUTH_SANITIZE_REDIRECTS = True
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login/'
SOCIAL_AUTH_LOGIN_URL = '/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/dashboard/'
