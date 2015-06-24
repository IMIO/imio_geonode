# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _
import logging
logger = logging.getLogger(__name__)

if "notification" in settings.INSTALLED_APPS:
    import notification

    if hasattr(notification, 'models'):
        def create_notice_types(app, created_models, verbosity, **kwargs):
            notification.models.NoticeType.create(
                "imio_succes",
                "Opération d'importation",
                "L'opération c'est correcement dérouler")
            notification.models.NoticeType.create(
                "iimio_error",
                "Opération d'importation",
                "Une erreur c'est produite")

        signals.post_syncdb.connect(
            create_notice_types,
            sender=notification.models)
        logger.info(
            "Notifications Configured for adminimio.management.commands")
else:
    logger.info(
        "Skipping creation of NoticeTypes for adminimio.management.commands,"
        " since notification app was not found.")
