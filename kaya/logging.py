import boto3
from decouple import config

LOG_GROUP_NAME = config("LOG_GROUP_NAME", default="kaya")
AWS_REGION_NAME = config("AWS_REGION_NAME", default="ap-southeast-1")

boto3_logs_client = boto3.client("logs", region_name=AWS_REGION_NAME)


def logging_setup():
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {'level': 'INFO', 'handlers': ['watchtower', 'console']},
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'watchtower': {
                'class': 'watchtower.CloudWatchLogHandler',
                'boto3_client': boto3_logs_client,
                'log_group_name': LOG_GROUP_NAME,
                'formatter': 'verbose',
                'level': 'INFO',
            },
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
                'formatter': 'verbose',
                "include_html": True,
            },
        },
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'loggers': {
            'django': {
                'level': 'INFO',
                'handlers': ['watchtower', 'console'],
                'propagate': True,
            },
        },
    }
    return LOGGING
