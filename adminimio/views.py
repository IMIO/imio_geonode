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
        print('   !!! request de type POST !!!')
        form = testForm(request.POST)
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
