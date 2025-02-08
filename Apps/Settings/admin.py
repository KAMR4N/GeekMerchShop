from django.contrib import admin
from .models import  *

# Register your models here.

class BannerAdmin(admin.ModelAdmin):
    list_display = ('image_alt','position')
    
    class Meta:
        model = Banner
        
class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ('image_alt','category')
    
    class Meta:
        model = CategoryImage        
        
admin.site.register(Banner, BannerAdmin)
admin.site.register(CategoryImage, CategoryImageAdmin)
admin.site.register(GeneralSettings)