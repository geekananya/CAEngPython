from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):        # change the django admin model display
    list_display = ('id', 'name', 'description', 'number_of_students', 'created_at')
    fields = ('name', 'description', 'number_of_students')

admin.site.register(Course, CourseAdmin)