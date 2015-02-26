from django.contrib import admin
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns
from adminimio.models import Im

class ImAdmin(admin.ModelAdmin):
    pass

admin.site.register(Im,ImAdmin)
