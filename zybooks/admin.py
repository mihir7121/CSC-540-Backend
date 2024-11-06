from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(TA)
admin.site.register(Course)
admin.site.register(Textbook)
admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Content)
admin.site.register(Activity)
admin.site.register(Question)
admin.site.register(Notification)
admin.site.register(Enrollment)
admin.site.register(Student)
admin.site.register(StudentPoints)