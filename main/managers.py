from django.db import models


class StoreAgentManager(models.Manager):
    def get_active_store(self):
        return self.filter(active=True)
