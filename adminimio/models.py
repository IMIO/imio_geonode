# -*- coding: utf-8 -*-
from django.db import models
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django import forms
from StringIO import StringIO
from slugify import slugify

from django.contrib.auth import get_user_model

from geonode.people.models import Profile
from geonode.groups.models import GroupProfile


class Im(models.Model):

    @staticmethod
    def updatelayer():
        out = StringIO()
        call_command('updatelayers', stdout=out)
        ret = out.getvalue() # Verifier pourquoi vide
        out.close()
        # recupere les infos de retour de methode
        created = 0
        updated = 0
        failed = 0
        return created, updated, failed

    def my_task_init(self):
        return mark_safe("<img class='loading' src='/static/img/loading.gif' alt='loading' style='display:none;' /><a data-identifier='task_%i' class='task'><img src='/static/img/process.png' style='cursor:pointer;' /></a>") % self.id
    my_task_init.allow_tags = True
    my_task_init.short_description = _(u"Execute Task")

    @staticmethod
    def crea_group_with_manager(name_user, name_group):
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

    @staticmethod
    def crea_group_with_manager_and_user(name_user, name_group):
        '''
        Methode de creation de groupe pour commune,
        Deux utilisateur y seront ajouter, un en user RO
        et un en manager RW
        '''
        # Recuperation de la surcharge de user
        User = get_user_model()


        u_ro = name_group+'_'+name_user
        u_rw = name_group+'_admin'

        g_user = name_group+'_ro'
        g_admin = name_group+'_rw'


        # Vérification de la disponibiliter des noms
        if Profile.objects.filter(username=u_ro).exists():
            raise Exception('Le nom d\'utilisateur généré est déjà utiliser')
        if Profile.objects.filter(username=u_rw).exists():
            raise Exception('Le nom d\'utilisateur généré est déjà utiliser')
        if GroupProfile.objects.filter(title=g_user).exists():
            raise Exception('Le nom de groupe généré est déjà utiliser')
        if GroupProfile.objects.filter(title=g_admin).exists():
            raise Exception('Le nom de groupe généré est déjà utiliser')
        
        # RW
        user_rw = User.objects.create_user(u_rw, None, u_rw)
        user_rw.save()

        group_admin = GroupProfile()
        group_admin.title = g_admin
        group_admin.slug = slugify(g_admin)
        group_admin.description = g_admin

        group_admin.save()

        group_admin.join(user_rw, role="manager")


        # RO
        user_ro = User.objects.create_user(u_ro, None, u_ro)
        user_ro.save()

        group_user = GroupProfile()
        group_user.title = g_user
        group_user.slug = slugify(g_user)
        group_user.description = g_user

        group_user.save()

        group_user.join(user_rw, role="manager")
        group_user.join(user_ro)


        user_rw.save()
        group_admin.save()

        user_ro.save()
        group_user.save()

        return True


    @staticmethod
    def addurb(in_user, in_password, in_dbadresse, in_dbname, in_dbuser, in_dbpassword, in_workspace, in_uri, in_groupname):
        out = StringIO()
        message = []
        if GroupProfile.objects.filter(title=in_groupname).exists():
            try:
                call_command('addurb',
                             stdout=out, 
                             geoserveradmin=in_user, 
                             gpw=in_password, 
                             urbanUrl=in_dbadresse, 
                             database=in_dbname, 
                             postuser=in_dbuser, 
                             ropw=in_dbpassword,
                             alias=in_workspace,
                             uri=in_uri,
                             groupname=in_groupname)
                ret = out.getvalue() # Verifier pourquoi vide
            except Exception as e:
                out.close()
                raise Exception (str(e))
            out.close()
        else:
            raise Exception('Le groupe n\'existe pas')
        return True, message


def profile_post_save(instance, sender, **kwargs):
    """En vue de recupere des infos lors de l ajout d un utilisateur"""

signals.post_save.connect(profile_post_save, sender=Profile)
