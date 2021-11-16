from django.db import models
from django.db.models.fields import CharField, TextField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth import get_user_model
from django.urls import reverse


class Snack(models.Model):
    title = CharField(max_length = 64)
    purchaser = ForeignKey(get_user_model(), on_delete = models.CASCADE)
    description = TextField(max_length = 256)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('snack_detail', args = [str(self.pk)])