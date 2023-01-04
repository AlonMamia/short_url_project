import datetime
from django.core.validators import URLValidator
from django.db import models


class Url(models.Model):
    # The original url that inserted to the db and been redirected from the tiny url
    original_url = models.URLField(null=False, validators=[URLValidator()])
    # The tiny url slug
    tiny_url = models.SlugField(max_length=30)
    # Counter of tiny_urls entries
    click_counter = models.IntegerField(default=0)

    class Meta:
        # The database table name
        db_table = 'urls_table'
        # Order the Url objects by click_counter in ascending order
        ordering = ['click_counter']
        # The app this model belongs to
        app_label = 'manage_urls'
