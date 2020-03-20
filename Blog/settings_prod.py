import datetime

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app_prod',
        'USER': 'root',
        'PASSWORD': 'admin123456',
        'HOST': '47.106.236.37',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'isolation_level': 'repeatable read',
        },
        'CONN_MAX_AGE': 12,
        'ATOMIC_REQUESTS': True
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://47.106.236.37:6379/7"],
        },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
        },
        'no_format': {
            # 只有日志时间的格式
            'format': '%(asctime)s\t%(message)s'
        },
        'console_print_format': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s] %(message)s'
        },
        'http_request': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(logCategory)s] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s] %(message)s'
        },
    },
    'filters': {
        'callback_filter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': [
                'Blog.utils.django_http_filter'
            ]
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/all.log',  # 日志输出文件
            'level': 'INFO',
            'maxBytes': 100 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/error.log',
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            # 请求处理
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
