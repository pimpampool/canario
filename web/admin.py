from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Lectura)
admin.site.register(Cryptocurrency)
admin.site.register(Address)
admin.site.register(PriceSnapshot)
