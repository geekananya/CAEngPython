from django.forms import ModelForm
from .models import Course



class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class LoginForm(ModelForm):
    pass