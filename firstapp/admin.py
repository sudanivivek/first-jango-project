from django.contrib import admin
from .models import Register

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','firstname','lastname','address','phone_number')  # Customize as needed
    search_fields = ('username', 'email','firstname','lastname','address','phone_number') 
# Register your models here.
admin.site.register(Register)


