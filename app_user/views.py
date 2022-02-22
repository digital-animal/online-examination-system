from django.shortcuts import render, redirect
from django.http import (
    HttpResponse,
    Http404,
    HttpResponseRedirect,
)

from .models import Student, Examiner

# Create your views here.
from .forms import (
    UserChoiceForm,
    StudentRegisterForm,
    ExaminerRegisterForm,
    UserLoginForm,
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

import cx_Oracle
from django.views.decorators.csrf import csrf_protect

# # register from and authentication - user defined

def create_username(first_name, last_name, user_number):
    # return f"{first_name.strip()}{last_name.strip()}_{str(user_number).strip()}"
    return f"{first_name.strip().lower()}{last_name.strip().lower()}"



def profile(request):
    connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
    cursor = connection.cursor()
    
    student_id=request.user.id
    examiner_id=request.user.id 

    request_student = Student.objects.filter(student_id=request.user.id).first()
    request_examiner = Examiner.objects.filter(examiner_id=request.user.id).first()
    
    
    # sql1 = """
    #     SELECT * FROM STUDENT
    #     WHERE student_id = :student_id
    # """
    # cursor.execute(sql1, [student_id])
    # request_student = cursor.fetchone()

    # sql2 = """
    #     SELECT * FROM STUDENT
    #     WHERE examiner_id = :examiner_id
    # """
    # cursor.execute(sql2, [examiner_id])
    # request_examiner = cursor.fetchone()

    # print(request_examiner)
    # print(request_student)
    # print(hasattr(request.user, 'username' ))
    # print(hasattr(request.user, 'email' ))

    template_name = 'app_user/profile.html'
    context = {
        "message": "",
        'user': request.user,
        'request_student': request_student,
        'request_examiner': request_examiner,
    }
    return render(request, template_name, context)

@csrf_protect
def register_choice(request):

    if request.method == "POST":
        choice_form = UserChoiceForm(request.POST)

        if choice_form.is_valid():

            role = choice_form.cleaned_data.get('role')

            print(role)
            if role == "Student":
                return redirect('register_student')

            elif role == "Examiner":
                return redirect('register_examiner')
        else:
            raise ValueError("Invalid form input")
        
    else:
        choice_form = UserChoiceForm()

    template_name = 'app_user/register_choice.html'
    context = {
        'choice_form': choice_form,
    }
    return render(request, template_name, context)


def register_student(request):

    connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
    cursor = connection.cursor()

    if request.method == "POST":
        student_form = StudentRegisterForm(request.POST)

        if student_form.is_valid():
             
            new_student = student_form.save(commit=False) # do this with raw sql

            # getting student dictionary for sql query

            student_info = student_form.cleaned_data
            
            first_name = student_info.get('first_name')
            last_name = student_info.get('last_name')
            student_number = student_info.get('student_number')
            new_username = create_username(first_name, last_name, student_number)
            print(new_username)

            new_student.username = new_username

            new_student.save()


            print(new_student.id)
            student_id = new_student.id 
            
            email = student_info.get('email')
            department_id = int(student_info.get('department'))

            sql = """
                INSERT INTO STUDENT (STUDENT_ID, FIRST_NAME, LAST_NAME, EMAIL, DEPARTMENT_ID) 
                VALUES (:student_id, :first_name, :last_name, :email, :department_id)
            """

            cursor.execute(sql, [student_id, first_name, last_name, email, department_id])
            connection.commit()
            # result = cursor.fetchall()
            cursor.close()

            print(student_info)

            return redirect('register_done')

        else:
            raise ValueError("Invalid form input")

    else:
        student_form = StudentRegisterForm()

    template_name = 'app_user/register_student.html'
    context = {
        'student_form': student_form,
    }
    return render(request, template_name, context)


def register_examiner(request):

    connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
    cursor = connection.cursor()

    if request.method == "POST":
        examiner_form = ExaminerRegisterForm(request.POST)

        if examiner_form.is_valid():

            new_examiner = examiner_form.save(commit=False) # dow this with raw sql

            examiner_info = examiner_form.cleaned_data

            first_name = examiner_info.get('first_name')
            last_name = examiner_info.get('last_name')
            examiner_number = examiner_info.get('examiner_number')
            new_username = create_username(first_name, last_name, examiner_number)

            new_examiner.username = new_username
            print(new_username)

            new_examiner.save()

            print(new_examiner.id)
            examiner_id = new_examiner.id
            # getting student dictionary for sql query
 
            email = examiner_info.get('email')
            department_id = int(examiner_info.get('department'))

            sql = """
                INSERT INTO EXAMINER (EXAMINER_ID, FIRST_NAME, LAST_NAME, EMAIL, DEPARTMENT_ID) 
                VALUES (:examiner_id, :first_name, :last_name, :email, :department_id)
            """


            cursor.execute(sql, [examiner_id, first_name, last_name, email, department_id])
            connection.commit()
            cursor.close()

            print(examiner_info)

            return redirect('register_done')

        else:
            raise ValueError("Invalid form input")

    else:
        examiner_form = ExaminerRegisterForm()

    template_name = 'app_user/register_examiner.html'
    context = {
        'examiner_form': examiner_form,
    }
    return render(request, template_name, context)


def register_done(request):

    template_name = 'app_user/register_done.html'
    context = {
        'message': 'Account created successfully.',
    }
    return render(request, template_name, context)


# # login from - user defined
@csrf_protect
def loginUser(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
        else:
            return HttpResponse("Username or Password doesn't match")

    else:
        form = UserLoginForm()

    template_name = "app_user/login.html"
    context = {
        'form': form,
    }

    return render(request, template_name, context)


def logoutUser(request):
    logout(request)

    template_name = 'app_user/logout.html'
    context = {
        'message': 'You are now logged out',
    }
    return render(request, template_name, context)
