from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    number_of_students = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}:{self.number_of_students}"