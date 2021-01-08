from django.contrib import admin

# Register your models here.
from .models import User_model,Note_model

admin.site.register(User_model)
admin.site.register(Note_model)