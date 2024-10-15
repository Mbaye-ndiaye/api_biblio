from django.apps import AppConfig


class TestdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testdb'
    
    def ready(self):
        import testdb.models
