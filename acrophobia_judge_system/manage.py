#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django

from django.db import models
from django.conf import settings

settings.configure(
        DEBUG=True,
        DATABASES={"default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:"
        }},
        INSTALLED_APPS=[__name__]
)

django.setup()


class Person(models.Model):
    MALE = 0
    FEMALE = 1

    # 名前
    name = models.CharField(max_length=128)
    # 性別
    sex = models.IntegerField(editable=False)
    # 日付
    date = models.DateTimeField()
    # 脈拍
    EEG = models.IntegerField(editable=False)
    # 脳波
    EFG = models.IntegerField(editable=False)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acrophobia_judge_system.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
