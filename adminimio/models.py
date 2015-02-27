# -*- coding: utf-8 -*-
from django.db import models
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

from geonode.people.models import Profile

class Im(models.Model):

    @staticmethod
    def updatelayer():
        print('   !!! dans updatelayer() de adminimio !!!')
        call_command('updatelayers')

    def my_task_init(self):
        return mark_safe("<img class='loading' src='/static/img/loading.gif' alt='loading' style='display:none;' /><a data-identifier='task_%i' class='task'><img src='/static/img/process.png' style='cursor:pointer;' /></a>") % self.id
    my_task_init.allow_tags = True
    my_task_init.short_description = _(u"Execute Task")


def profile_post_save(instance, sender, **kwargs):
    """En vue de recupere des infos lors de l ajout d un utilisateur"""
    print('   !!! On a recupere un signal profile_post_save, sender=Profile !!!')

signals.post_save.connect(profile_post_save, sender=Profile)
