from django.db import models
from django.contrib.auth import get_user, get_user_model
import uuid
from django.urls import reverse_lazy
from django.utils import timezone
User = get_user_model()


class EventsModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    detail = models.TextField(null=True, blank=True)
    evaluation = models.PositiveSmallIntegerField(default=0)
    date_at = models.DateField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.title
# Create your models here.
