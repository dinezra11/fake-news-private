from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserData


# Register your models here.
@admin.register(UserData)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
                    UserData._meta.get_fields()]
