# -*- coding: utf-8 -*-
import os
import sys
import logging
import shutil
import traceback

from django.shortcuts import render

from adminimio.models import Im

#def index(request):
#    posts = Post.objects.filter(published=True)
#    return render(request,'blog/index.html',{'posts':posts})
