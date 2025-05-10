# users/apps.py

from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'       # must match your app folder!
    
    def ready(self):
        # Import signals to register the handler
        import users.signals