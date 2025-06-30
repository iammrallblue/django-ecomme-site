from django.contrib import admin
from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_active',
                    'is_staff', 'is_superuser')
    list_display_links = ('id', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    list_per_page = 20


# If you want a simple registration:
# admin.site.register(User)
