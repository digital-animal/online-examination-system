from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    department_id = models.FloatField(primary_key=True)
    department_code = models.CharField(max_length=32)
    department_name = models.CharField(max_length=128)

    class Meta:
        managed = True
        db_table = 'department'

    def __str__(self):
        return f"{self.department_name} ({self.department_code})"


class Course(models.Model):
    course_id = models.FloatField(primary_key=True)
    course_code = models.CharField(max_length=32)
    course_name = models.CharField(max_length=128)
    department = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'course'

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"



class Question(models.Model):
    question_id = models.FloatField(primary_key=True)
    question_text = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    examiner = models.ForeignKey("app_user.Examiner", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'question'

    def __str__(self):
        return f"{self.question_id}. {self.question_text}"



class Choice(models.Model):
    choice_id = models.FloatField(primary_key=True)
    choice_text = models.CharField(max_length=256)
    is_correct = models.FloatField(default=0)
    question = models.ForeignKey(Question, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'choice'


# class Exam(models.Model):
#     exam_id = models.FloatField(primary_key=True)
#     exam_duration = models.FloatField(blank=True, null=True)
#     exam_marks = models.FloatField(blank=True, null=True)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
#     question = models.ManyToManyField(Question, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'exam'

#     def __str__(self):
#         return f"{self.course}"



# class Result(models.Model):
#     result_id = models.FloatField(primary_key=True)
#     obtained_marks = models.FloatField(blank=True, null=True)
#     obtained_grade = models.CharField(max_length=10, blank=True, null=True)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)


#     class Meta:
#         managed = True
#         db_table = 'result'

#     def __str__(self):
#         return f"{self.result_id} - {self.exam}"


















