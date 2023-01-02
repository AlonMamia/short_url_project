import datetime
from django.core.validators import URLValidator
from django.db import models


# Create your models here.
class Url(models.Model):
    original_url = models.URLField(null=False, validators=[URLValidator()])
    tiny_url = models.SlugField(max_length=30)
    click_counter = models.IntegerField(default=0)

    class Meta:
        db_table = 'urls_table'
        ordering = ['click_counter']
        app_label = 'manage_urls'







