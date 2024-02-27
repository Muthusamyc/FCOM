import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENVIRONMENT = {
    "production": {
        "DEBUG": False,
        "ALLOWED_HOSTS": [
            "*"
        ],
        "DATABASES": {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": "fcom",
                "USER": "fcom_admin",
                "PASSWORD": "fcom_admin@23_secure",
                "HOST": "localhost",
                "PORT": "3306",
            }
        },
        "CSRF_TRUSTED_ORIGINS": ["https://fcomindia.com", "http://fcomindia.com", "164.52.216.133"],
    },
    "stagging": {
        "DEBUG": True,
        "ALLOWED_HOSTS": ["*"],
        "DATABASES": {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            },
        },
    },
    "development": {
        "DEBUG": True,
        "ALLOWED_HOSTS": ["*"],
        "DATABASES": {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
    },
}
