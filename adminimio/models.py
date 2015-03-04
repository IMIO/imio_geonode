# -*- coding: utf-8 -*-
from django.db import models
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django import forms

from django.contrib.auth.models import User

from geonode.people.models import Profile
from geonode.groups.models import GroupProfile


class Im(models.Model):

    @staticmethod
    def updatelayer():
        print('   !!! dans updatelayer() de adminimio !!!')
        call_command('updatelayers')

    def my_task_init(self):
        return mark_safe("<img class='loading' src='/static/img/loading.gif' alt='loading' style='display:none;' /><a data-identifier='task_%i' class='task'><img src='/static/img/process.png' style='cursor:pointer;' /></a>") % self.id
    my_task_init.allow_tags = True
    my_task_init.short_description = _(u"Execute Task")

    @staticmethod
    def crea_group_with_manager(name_user, name_group):
        print('    !!! dans crea_group_with_manager() de adminimio !!!')
        user = User.objects.create_user(name_user, 'lennon@thebeatles.com', name_user)
        user.is_staff = True
        #user.save(using=self._db)
        geonode_user = Profile(user)

        group = GroupProfile()
        group.join(geonode_user)


def profile_post_save(instance, sender, **kwargs):
    """En vue de recupere des infos lors de l ajout d un utilisateur"""
    print('   !!! On a recupere un signal profile_post_save, sender=Profile !!!')

signals.post_save.connect(profile_post_save, sender=Profile)


class ValifdForm(forms.Form):
    csrf_token = forms.CharField()
