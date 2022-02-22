from django.contrib import admin

from .models import (
    Department,
    Course,
    Question,
    Choice,
)

admin.site.register(Department)


class CourseAdmin(admin.ModelAdmin):
    fields = [
        'course_id',
        'course_code',
        'course_name',
        'department',
    ]

admin.site.register(Course, CourseAdmin)



class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = [
        'choice_text',
        'is_correct',
    ]
    extra = 0
    max_num = 4


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question_id',
        'question_text',
    )
    list_display_links = ('question_text',)
    list_per_page = 20
    ordering = ['question_id']

    fields = [
        'course',
        'examiner',
        'question_text',
    ]

    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)

# admin.site.register(Choice)
