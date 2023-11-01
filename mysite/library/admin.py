
from django.contrib import admin

from .models import *

admin.site.register(Users)
admin.site.register(Authors)
admin.site.register(Books)
admin.site.register(Borrow)
admin.site.register(Fines)



