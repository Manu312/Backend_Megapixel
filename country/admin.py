from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Country

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name_common', 'capital', 'continent')