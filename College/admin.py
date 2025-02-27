from django.contrib import admin
from .models import BannerUpload

@admin.register(BannerUpload)
class BannerUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at','banner1','banner2','banner3','open_image')

    
