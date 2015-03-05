# -*- coding: utf-8 -*-
from django.db import models
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django import forms
from slugify import slugify

from django.contrib.auth import get_user_model

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
        # Recuperation de la surcharge de user
        User = get_user_model()

        # Test si nom user est deja prit
        lUser = list(User.objects.all())
        for u in lUser:
           if u.name_long == name_user:
              raise Exception('That user name already exists')

        lGroup = list(GroupProfile.objects.all())
        for g in lGroup:
            if g.title == name_group or g.slug == slugify(name_group):
              raise('That group name already exists')

        user = User.objects.create_user(name_user, None, name_user)
        user.is_staff = True
        user.save()

        group = GroupProfile()
        group.title = name_group
        group.slug = slugify(name_group)
        group.description = name_group

        group.save()

        group.join(user, role="manager")

        user.save()
        group.save()

        return True


def profile_post_save(instance, sender, **kwargs):
    """En vue de recupere des infos lors de l ajout d un utilisateur"""
    print('   !!! On a recupere un signal profile_post_save, sender=Profile !!!')

signals.post_save.connect(profile_post_save, sender=Profile)

