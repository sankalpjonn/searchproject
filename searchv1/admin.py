from django.contrib import admin
from models import Image

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ['url', 'local_filename', 'meta_data']
    list_display = ['url', 'admin_thumbnail']

admin.site.register(Image, ImageAdmin)
