from django.contrib.auth.models import User
from django.db import models


class UserAnalytics(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    last_request_at = models.DateTimeField(default=None, blank=True, null=True)
