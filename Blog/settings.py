import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!b2u9toio=9nxdy(vh&_k)p^@(a0--b8=-rh(j+$8^u4&24%20'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'BlogFront',
    'Wx',
    'Bus',
    # 'Learn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# SECURE_REQUIRED_PATHS = (
#     '/admin',
# )

ROOT_URLCONF = 'Blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/htmls'), os.path.join(BASE_DIR, 'templates/htmls_t')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'Blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wx',
        'USER': 'root',
        'PASSWORD': '13486059134chen',
        'HOST': '47.106.236.37',
        'PORT': '3306',
        'CONN_MAX_AGE': 700,
    },
    # 'db_note': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'blog',
    #     'USER': 'shawjean',
    #     'PASSWORD': '13486059134',
    #     'HOST': '119.23.216.166',
    #     'PORT': '3306'
    # }
}
DATABASE_ROUTERS = ['Blog.database_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    # 'Wx': 'default',
    'BlogFront': 'db_note'
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('\\', '/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')     #设置静态文件路径为主目录下的media文件�?

STATICFILES_DIRS = [
    'Bus/static_bus',
    'BlogFront/static',
]
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
LOGIN_URL = '/login'


