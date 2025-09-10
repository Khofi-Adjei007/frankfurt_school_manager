from django.apps import AppConfig

class ModeratorsServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'moderator.moderators_service'
    label = 'moderators_service'
    verbose_name = "Moderators Service"