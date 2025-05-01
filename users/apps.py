from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"


    def ready(self):
        import users.signals
        # This method is called when the app is ready
        # You can use it to perform any initialization tasks
