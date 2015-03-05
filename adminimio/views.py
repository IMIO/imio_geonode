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

from adminimio.models import Im
from adminimio.forms import ValidFormUpdatelayer, ValidFormCommuneUser


def is_auth(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """
    def _checklogin(request, *args, **kwargs):
        print('   !!! _checklogin() !!!')
        if request.user.is_active and request.user.is_staff:
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
    print('   !!! admin_view_imio() !!!')
    if request.method == 'POST':
        out['success'] = False
        print('   !!! request de type POST !!!')
        token_session = request.token
        form = ValidFormUpdateLayer(request.POST)
        if form.is_valid():
            if csrf_token in request.POST:
                form_token = form.cleaned_data['csrf_token']
                request_token = request.POST['csrf_token']
                if form_token == request_token :
                    # La methode de mise jour
                    Im.updatelayer()
                    out['success'] = True

        return HttpResponse(
            json.dumps(out),
            mimetype='application/json',
            status=status_code)
    else:
        print('   !!! request de type GET !!!')
        return render_to_response(template, RequestContext(request, out))

@is_auth
def admin_view_imio_action(request, template='adminimio/imio_management.html'):
    print('   !!! admin_view_imio_action() !!!')
    out = {}
    Im.updatelayer()
    return render_to_response(template, RequestContext(request, out))






@is_auth
def admin_view_crea_group_with_manager(request, template='adminimio/imio_management_commune.html'):
    result = False
    out = {}
    print('   !!! admin_view_crea_group_with_manager() !!!')
    if request.method == 'POST':
        out['success'] = False
        print('   !!! request de type POST !!!')
        #token_session = request.token
        form = ValidFormCommuneUser(request.POST)

        if form.is_valid():
            form_token = form.cleaned_data['csrf_token']
            user_name = form.cleaned_data['in_user']
            comm_name = form.cleaned_data['in_comm']
            
            try:
               result = Im.crea_group_with_manager(user_name,comm_name)
            except Exception as e:
                out['error'] = str(e.message)

        if result == True:
            out['success'] = True
            status_code = 200
        else:
            status_code = 500

        print(out)
        return HttpResponse(
            json.dumps(out),
            mimetype='application/json',
            status=status_code)
    else:
        print('   !!! request de type GET !!!')
        return render_to_response(template, RequestContext(request, out))
