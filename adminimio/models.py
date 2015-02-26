from django.db import models
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _

class Im(models.Model):

    @staticmethod
    def updatelayer():
        call_command('updatelayers')

    def my_task_init(self):
        return mark_safe("<img class='loading' src='/static/img/loading.gif' alt='loading' style='display:none;' /><a data-identifier='task_%i' class='task'><img src='/static/img/process.png' style='cursor:pointer;' /></a>") % self.id
    my_task_init.allow_tags = True
    my_task_init.short_description = _(u"Execute Task")
