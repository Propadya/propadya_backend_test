"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.
For more information, see:
https://docs.djangoproject.com/en/5.1/topics/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from decouple import config

# ======== Base Directories ========
BASE_DIR = Path(__file__).resolve().parent.parent

# ======== Environment Variables ========
LOCAL = config("LOCAL", cast=bool, default=False)
STAGING = config("STAGING", cast=bool, default=False)
PRODUCTION = config("PRODUCTION", cast=bool, default=False)
DEBUG = config("DEBUG", cast=bool, default=True)
# ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=["localhost"],
#                        cast=lambda v: [url.strip() for url in v.split(",")])
if STAGING:
    ALLOWED_HOSTS = ["147.182.165.199", "staging.backend.propadya.com", "www.staging.backend.propadya.com"]
elif PRODUCTION:
    ALLOWED_HOSTS = ["147.182.165.199", "prod.backend.propadya.com", "www.prod.backend.propadya.com"]
else:
    ALLOWED_HOSTS = ["*"]

FRONTEND_URL = "http://localhost:3000"
if PRODUCTION:
    FRONTEND_URL = "https://app.propadya.com"
elif STAGING:
    FRONTEND_URL = "https://staging.propadya.com"

# ======== Secret Key ========
SECRET_KEY = config("SECRET_KEY", default="django-insecure-default-key")

# ======== Installed Apps ========
CUSTOM_APPS = [
    "base",
    "event",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True


# ======== Middleware ========
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "base.middleware.online_user.OnlineUserMiddleware",
]

# ======== URL and WSGI Config ========
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ======== Templates ========
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ======== Database ========
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default=""),
        "USER": config("DB_USER", default=""),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", cast=int, default=5432),
        "OPTIONS": {
            "sslmode": "verify-full" if config("SSL", cast=bool, default=False) else None,
            "sslrootcert": "/ssl/ca-certificate.crt" if config("SSL", cast=bool, default=False) else None,
        },
    }
}

# ======== Authentication ========
# AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "base.validators.StrongPasswordValidator"},
]

# ======== Static and Media Files ========
STATIC_ROOT = os.path.join(BASE_DIR, "staticfolders")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"
else:
    from config.storage_config import *  # Use external storage config for production


# ======== REST Framework ========
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        # "base.authentication.CustomJWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_PAGINATION_CLASS": "base.pagination.CustomPagination",
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "utils.custom_exception_handler.custom_exception_handler",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "COERCE_DECIMAL_TO_STRING": False,
    # "DEFAULT_THROTTLE_CLASSES": [
    #         "rest_framework.throttling.AnonRateThrottle",
    #         "rest_framework.throttling.UserRateThrottle",
    #     ],
    # "DEFAULT_THROTTLE_RATES": {
    #     "anon": "5/minute",
    #     "user": "10/minute",
    # }
}

SIMPLE_JWT = {
    # Shorter lifespan for access tokens to reduce exposure window
    "ACCESS_TOKEN_LIFETIME":  timedelta(minutes=10) if PRODUCTION else timedelta(days=6),  # Reduce access token lifetime
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),     # Maintain refresh token lifespan

    # Rotate refresh tokens upon each use
    "ROTATE_REFRESH_TOKENS": True,

    # Blacklist old refresh tokens after they are rotated
    "BLACKLIST_AFTER_ROTATION": True,

    # Secure the token signature with a unique key
    "SIGNING_KEY": SECRET_KEY,
    "ALGORITHM": "HS256",  # Default, can be changed to RS256 for asymmetric encryption

    # Include a JTI (unique token identifier) for token blacklisting
    "JTI_CLAIM": "jti",
    # 'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    # Secure cookies for better token storage
    # "AUTH_COOKIE_NAME": "access_token",
    # "AUTH_COOKIE_SECURE": True,  # Ensures HTTPS is used for cookies
    # "AUTH_COOKIE_HTTP_ONLY": True,  # Prevents JavaScript from accessing cookies
    # "AUTH_COOKIE_SAMESITE": "Lax",  # Restricts cross-origin requests

    # Enforce audience and issuer for better token validation
    # "AUDIENCE": "your-audience",  # Specify intended audience
    # "ISSUER": "your-issuer",      # Specify token issuer

    # Enable sliding token expiration
    # "SLIDING_TOKEN_LIFETIME": timedelta(minutes=15),
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=7),
}
# ======== Swagger and Spectacular ========
SPECTACULAR_SETTINGS = {
    "TITLE": "Propadya APIs",
    "DESCRIPTION": "Propadya API's for developer",
    "VERSION": "1.0",
    "SCHEMA_PATH_PREFIX": r"/api/+",
    # available SwaggerUI configuration parameters
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    "PARSER_WHITELIST": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'docExpansion': 'none',
        # To prevent schema to be appeared uncomment the following
        # 'defaultModelsExpandDepth': -1,
    },
    'DEFAULT_AUTO_SCHEMA': 'drf_spectacular.openapi.AutoSchema',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PUBLIC': True,
    'USE_SESSION_AUTH': False,
    'REDUCER': 'drf_spectacular.reducing.RouterDepthReducer',
    'COMPONENT_SPLIT_REQUEST': True,

    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest",
    "SWAGGER_UI_FAVICON_HREF": STATIC_URL + "images/api.ico",

    'DEFAULT_FIELD_INSPECTORS': [
        'drf_spectacular.inspectors.CamelCaseJSONFilter',
        'drf_spectacular.inspectors.InlineSerializerInspector',
        'drf_spectacular.inspectors.RelatedFieldInspector',
        'drf_spectacular.inspectors.ChoiceFieldInspector',
        'drf_spectacular.inspectors.FileFieldInspector',
        'drf_spectacular.inspectors.DictFieldInspector',
        'drf_spectacular.inspectors.SimpleFieldInspector',
        'drf_spectacular.inspectors.StringDefaultFieldInspector',
    ],
    "SECURITY_DEFINITIONS": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    },
    # "AUTHENTICATION_CLASSES": [
    #     "base.authentication.CustomJWTAuthenticationScheme",
    # ],
    "SECURITY": [{"BearerAuth": []}],

}

# ======== Logging ========
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
