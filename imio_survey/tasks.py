# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail
from django.db import transaction

logger = get_task_logger(__name__)

@shared_task
def mul(x, y):
    return x * y
