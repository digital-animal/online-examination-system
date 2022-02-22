from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import User

from app_exam.models import Department
# Create your models here.

class Student(models.Model):
    # student_id = models.FloatField(primary_key=True, unique=True)
    student = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128) 
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'student'

    def __str__(self):
        return f"{self.first_name} {self.last_name}".title()


class Examiner(models.Model):
    # examiner_id = models.FloatField(primary_key=True, unique=True)
    examiner = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128) 
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'examiner'

    def __str__(self):
        return f"{self.first_name} {self.last_name}".title()
