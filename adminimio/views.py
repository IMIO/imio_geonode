# -*- coding: utf-8 -*-
import os
import sys
import logging
import shutil
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.utils import simplejson as json
from django.utils.html import escape
from django.template.defaultfilters import slugify
from django.forms.models import inlineformset_factory
from django.db.models import F
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from functools import wraps
from django.core.context_processors import csrf

from adminimio.models import Im
from adminimio.forms import *


def is_auth(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.groups.filter(name='imio').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse(
            loader.render_to_string(
                '401.html', RequestContext(
                    request, {
                        'error_message': _("You are not allowed to view this page.")})), status=403)

    return wraps(view_func)(_checklogin)


@is_auth
def admin_view_imio(request, template='adminimio/imio_management.html'):
    out = {}
    return render_to_response(template, RequestContext(request, out))


@is_auth
def admin_view_updatelayer(request, template='adminimio/imio_management_updatelayer.html'):
    result = False
    out = {}
    if request.method == 'POST':
        out['success'] = False
        #token_session = request.token
        form = ValidFormUpdateLayer(request.POST)
        if form.is_valid():
            form_token = form.cleaned_data['csrf_token']
            try:
                created, updated, failed = Im.updatelayer()
                result = True
                out['success'] = True
            except Exception as e:
                out['error'] = str(e.message)
        else:
            out['error'] = "Des paramètres sont manquant"
        if result == True:
            out['success'] = True
            status_code = 200
            message = 'Mise à jour réussie'
            messages.success(request, message)
            return render_to_response(template, RequestContext(request, out))
        else:
            status_code = 500
            message = out['error']
            messages.error(request, message)
            return render_to_response(template, RequestContext(request, out))

        return HttpResponse(
            json.dumps(out),
            mimetype='application/json',
            status=status_code)
    else:
        out.update(csrf(request))
        return render_to_response(template, RequestContext(request, out))

@is_auth
def admin_view_crea_group_with_manager(request, template='adminimio/imio_management_commune.html'):
    result = False
    out = {}
    if request.method == 'POST':
        out['success'] = False
        #token_session = request.token
        form = ValidFormCommuneUser(request.POST)

        if form.is_valid():
            form_token = form.cleaned_data['csrf_token']
            user_name = form.cleaned_data['in_user']
            comm_name = form.cleaned_data['in_comm']
            
            try:
               result = Im.crea_group_with_manager_and_user(user_name,comm_name)
            except Exception as e:
                out['error'] = str(e.message)

        else:
            out['error'] = "Des paramètres sont manquant"

        if result == True:
            out['success'] = True
            status_code = 200
            message = 'Groupes et utilisateurs crée'
            messages.success(request,message)
            return render_to_response(template, RequestContext(request, out))
        else:
            status_code = 500
            message = out['error']
            messages.error(request,message)
            return render_to_response(template, RequestContext(request, out))

        return HttpResponse(
            json.dumps(out),
            mimetype='application/json',
            status=status_code)
    else:
        out.update(csrf(request))
        return render_to_response(template, RequestContext(request, out))


@is_auth
def admin_view_addurb(request, template='adminimio/imio_management_addurb.html'):
    result = False
    out = {}
    if request.method == 'POST':
        out['success'] = False
        #token_session = request.token
        form = ValidFormAddurb(request.POST)

        if form.is_valid():
            form_token = form.cleaned_data['csrf_token']
            in_user = form.cleaned_data['in_user']
            in_password = form.cleaned_data['in_password']
            in_dbadresse = form.cleaned_data['in_dbadresse']
            in_dbname = form.cleaned_data['in_dbname']
            in_dbuser = form.cleaned_data['in_dbuser']
            in_dbpassword = form.cleaned_data['in_dbpassword']
            in_workspace = form.cleaned_data['in_workspace']
            in_uri = form.cleaned_data['in_uri']
            in_groupname = form.cleaned_data['in_groupname']
            try:
                result, message = Im.addurb(in_user, in_password, in_dbadresse, in_dbname, in_dbuser, in_dbpassword, in_workspace, in_uri, in_groupname)
            except Exception as e:
                out['error'] = str(e.message)
        else:
            out['error'] = "Des paramètres sont manquant"

        if result == True:
            out['success'] = True
            message = 'Récuperation des couches terminée'
            messages.success(request,message)
            return render_to_response(template, RequestContext(request, out))
            status_code = 200
        else:
            status_code = 500
            message = out['error']
            messages.error(request,message)
            return render_to_response(template, RequestContext(request, out))

        return HttpResponse(
            json.dumps(out),
            mimetype='application/json',
            status=status_code)
    else:
        out.update(csrf(request))
        return render_to_response(template, RequestContext(request, out))
