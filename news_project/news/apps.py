from django.apps import AppConfig
from django.contrib.auth.models import Group

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from .templatetags.censor import censor
        from django.template import Library

        Library().filters['censor'] = censor

class MyAppConfig(AppConfig):
    name = 'news'

    def ready(self):
        common_group, _ = Group.objects.get_or_create(name='common')
        authors_group, _ = Group.objects.get_or_create(name='authors')








