from django.contrib import admin
from .models import Country

class CountryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Country, CountryAdmin)

# 'Countrys' 텍스트를 'Countries'로 수정
admin.site.verbose_name_plural = 'Countries'
