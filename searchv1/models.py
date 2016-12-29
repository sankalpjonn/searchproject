from __future__ import unicode_literals
from django.db import models
from jsonfield import JSONField

class Image(models.Model):
    url = models.CharField(max_length=255)
    local_filename = models.CharField(max_length=50, primary_key=True)
    meta_data = JSONField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def admin_thumbnail(self):
        return u'<img src="%s" />' % ("http://104.198.45.236/images/" + self.local_filename)

    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True
