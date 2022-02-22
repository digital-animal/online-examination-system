from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('create-exam/', views.create_exam, name='create_exam'),
    path('mcq/<int:course_id>/<int:marks>', views.mcq, name='mcq'),

    path('add-question/', views.add_question, name='add_question'),
    path('add-choice/', views.add_choice, name='add_choice'),
    path('add-question/done/', views.add_question_done, name='add_question_done'),

    path('edit-question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('edit-choice/', views.edit_choice, name='edit_choice'),

    path('query-question/', views.query_question, name='query_question'),
    path('show-question/<int:course_id>/<int:examiner_id>/', views.show_question, name='show_question'),

    path('edit-question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('edit-question/done/', views.edit_question_done, name='edit_question_done'),

    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('delete-question/done/', views.delete_question_done, name='delete_question_done'),

    path('result/', views.result, name='result'),
]
