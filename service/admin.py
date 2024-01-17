from django.contrib import admin
from service.models import Category,Review,Service,Cart

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Review)
admin.site.register(Service)
admin.site.register(Cart)