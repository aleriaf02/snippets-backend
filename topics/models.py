from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=30, blank=False)
    color = models.CharField(max_length=7, blank=False, default='')
    icon = models.ImageField(upload_to='static/topics/', blank=True)

    class Meta:
        ordering = ['-id']
