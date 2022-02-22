from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    # register
    path('register/choice/', views.register_choice, name='register_choice'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/examiner/', views.register_examiner, name='register_examiner'),
    path('register/done/', views.register_done, name='register_done'),

    # # user defined login and logout
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    # # profile info update
    path('profile/', views.profile, name="profile"),
    # path('profile/student/', views.student_profile, name="student-profile"),
    # path('profile/examiner/', views.examiner_profile, name="examiner-profile"),

    # # password change
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name="app_user/password_change_form.html"), name="password_change"),    
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="app_user/password_change_done.html"), name="password_change_done"),

]
