
from django.contrib import admin

from .models import Students,Borrow,Books,Authors,Fines,Faculty,BookIssues

admin.site.register(Students)
admin.site.register(Faculty)
admin.site.register(Authors)
admin.site.register(Books)
admin.site.register(Borrow)
admin.site.register(BookIssues)
admin.site.register(Fines)



