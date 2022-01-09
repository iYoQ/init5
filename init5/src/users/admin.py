from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username','date_registration','last_login','role','is_staff','is_active','description','birth_date','is_newsmaker','hide_email')
    list_filter = ('date_registration', )
    search_fields = ('username', )

admin.site.register(User, UserAdmin)
