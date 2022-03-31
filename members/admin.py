from django.contrib import admin
from .models import Gender, Client


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = [('name', 'slug'), 'is_active', ('created', 'updated')]
    list_display = ['name', 'is_active', 'created']
    list_display_links = ['name']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created', 'updated']
    save_as = True
    search_fields = ['name']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = ['user', ('last_name', 'first_name'), 'gender', 'photo', ('longitude', 'latitude'), 'is_active',
              ('created', 'updated')]
    list_display = ['min_photo', 'user', 'last_name', 'first_name', 'get_longitude_latitude', 'gender', 'is_active',
                    'created', 'updated']
    list_display_links = ['user']
    list_editable = ['last_name', 'first_name', 'gender', 'is_active']
    list_filter = ['gender']
    readonly_fields = ['created', 'updated']
    save_as = True
    search_fields = ['last_name']
