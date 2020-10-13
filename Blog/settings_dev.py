import datetime

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'app_prod',
        'USER': 'root',
        'PASSWORD': '1996Chan',
        'HOST': '81.68.205.132',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'isolation_level': 'repeatable read',
        },
        'CONN_MAX_AGE': 12,
        'ATOMIC_REQUESTS': True
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '\033[22;36;m%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s\033[0m'
        },
        'no_format': {
            # 只有日志时间的格式
            'format': '%(asctime)s\t%(message)s'
        },
        'console_print_format': {
            'format': '\033[22;36;m%(asctime)s [%(threadName)s:%(thread)d] [%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s] %(message)s\033[0m'
        },
        'http_request': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(logCategory)s] [%(requestId)s] [%(IMEI)s] [%(APP_PLATFORM)s:%(APP_VERSION)s] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s] [%(userName)s:%(userId)s:%(termUserId)s] %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/all.log',  # 日志输出文件
            'maxBytes': 100 * 1024 * 1024,  # 文件大小
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
        'console_print': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_print_format'
        },
        'time_request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/time_request.log',
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'no_format',
        },
        'http_request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/request.log',
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'http_request',
            'encoding': 'utf-8',
        },
        'http_login_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/login_request.log',
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'http_request',
            'encoding': 'utf-8',
        },
        'db_opt_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/db_operation_log.log',
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'http_request',
            'encoding': 'utf-8',
        },
        'permission_denied_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/permission_denied.log',
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'no_format',
        },
        'business_error_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/business_error.log',
            'maxBytes': 1024 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'no_format',
        },
    },
    'loggers': {
        # 'biz.error.logger':{
        #     'django': {
        #         'handlers': ['default', 'console','biz.error'],
        #         'level': 'DEBUG',
        #         'propagate': False
        #     },
        # },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'django.request': {
            # 请求处理
            'handlers': ['console', 'error', 'default'],
            'level': 'INFO',
            'propagate': False,
        },
        # 'time.request': {
        #     # 时间统计
        #     'handlers': ['time_request_handler'],
        #     'level': 'DEBUG',
        #     'propagate': True
        # },
        'console_print': {
            # 控制台输出
            'handlers': ['console_print'],
            'level': 'INFO',
            'propagate': True
        },
        'http.request': {
            # http请求
            'handlers': ['http_request_handler'],
            'level': 'INFO',
            'propagate': True
        },
        'db_opt': {
            'handlers': ['db_opt_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'http.login': {
            # 登录
            'handlers': ['http_login_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'permission_denied': {
            'handlers': ['permission_denied_handler'],
            'level': 'ERROR',
            'propagate': True
        },
        'business_error': {
            'handlers': ['business_error_handler'],
            'level': 'ERROR',
            'propagate': True
        },
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

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/0",
#         # "LOCATION": "redis://:tigershi,,@112.13.89.82:6379/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "CONNECTION_POOL_KWARGS": {"max_connections": 20}
#         }
#     }
# }