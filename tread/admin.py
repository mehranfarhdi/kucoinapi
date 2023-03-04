from django.contrib import admin

# Register your models here.
from .models import Coin, ExitAndEnterFactor

admin.site.register(Coin)
admin.site.register(ExitAndEnterFactor)
