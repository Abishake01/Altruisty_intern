from django.contrib import admin
from .models import bannerupload

class CollegeBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at')
    
    def save_model(self, request, obj, form, change):
        if request.FILES.get('image'): 
            obj.image = request.FILES['image'].read()  # Convert image to binary
        super().save_model(request, obj, form, change)

admin.site.register(bannerupload, CollegeBannerAdmin)
