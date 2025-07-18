from django.contrib import admin
from .models import Category  # ✅ Use correct class name (capital C)

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name', )}
list_display = ('category_name', 'slug')


# Register the model with the custom admin class
admin.site.register(Category, CategoryAdmin)
