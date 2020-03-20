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
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/all.log',  # 日志输出文件
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
            'handlers': ['console', 'default'],
            'level': 'DEBUG',
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
            'level': 'DEBUG',
            'propagate': True
        },
        'http.request': {
            # http请求
            'handlers': ['http_request_handler'],
            'level': 'DEBUG',
            'filters': ['callback_filter'],
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
