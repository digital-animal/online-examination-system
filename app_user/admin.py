from django.contrib import admin

from .models import (
    Student,
    Examiner,
    # Exam,
    # Result,
    # ExamQuestionPaper,
    # Person
)
# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    # list_display = (
    #     'student_id',
    #     'student_name',
    # )

    # list_display_links = ('student_id', 'student_name',)
    # list_per_page = 20

    exclude = ('student_number',)
    
admin.site.register(Student, StudentAdmin)


class ExaminerAdmin(admin.ModelAdmin):
    # list_display = (
    #     # 'examiner_id',
    #     'examiner_name',
    # )

    # list_display_links = (
    #     # 'examiner_id', 
    #     'examiner_name',
    #     )
    # list_per_page = 20

    exclude = ('examiner_number',)

admin.site.register(Examiner, ExaminerAdmin)
