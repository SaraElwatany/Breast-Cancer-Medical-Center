from django.apps import AppConfig
from django.dispatch import receiver
from django.core.signals import request_started


#class HospitalConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    #name = 'hospital'

    #def ready(self):
        #@receiver(request_started)
        #def start_server(sender, **kwargs):
            #from django.core.management import call_command
            #call_command('rundevscript')


class HospitalConfig(AppConfig):
    name = 'hospital'
