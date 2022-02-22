from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
)

from .models import Student, Examiner

import cx_Oracle

def get_departments():
    connection = cx_Oracle.connect("dj/dj@localhost:1521/ORCLPDB", encoding="UTF-8")
    cursor = connection.cursor()

    sql = "SELECT * FROM DEPARTMENT"

    cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()
    cursor.close()

    di = {}
    li = []

    for record in result:
        dept_id = record[0]
        # dept_code = record[1]
        dept_name = record[2]
        # di[dept_id] = dept_code
        # di[dept_code] = dept_name
        di[dept_id] = dept_name

    for key, value in di.items():
        li.append(tuple([key, value]))

    t = tuple(li)

    return t


class UserChoiceForm(forms.Form):

    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Examiner', 'Examiner'),
    )

    role = forms.ChoiceField(
        label="Role",
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
    )


class StudentRegisterForm(UserCreationForm):

    DEPARTMENTS = get_departments()

    username = forms.CharField(
        label="Username",
        max_length=100,
        required=False,
        widget = forms.HiddenInput(),
    )

    student_number = forms.IntegerField(
        label="Student Number",
        required=True,
        widget=forms.NumberInput,
    )

    first_name = forms.CharField(
        label="First Name",
        max_length=128,
        required=True,
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=128,
        required=True,
    )

    email = forms.EmailField(
        label="Email",
        max_length=128,
        required=True,
    )

    department = forms.ChoiceField(
        label="Department",
        choices=DEPARTMENTS,
    )

    password1 = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + (
            'student_number',
            'first_name',
            'last_name',
            'email',
            'department',
        )



class ExaminerRegisterForm(UserCreationForm):

    DEPARTMENTS = get_departments()


    username = forms.CharField(
        label="Username",
        max_length=100,
        required=False,
        widget = forms.HiddenInput(),
    )

    examiner_number = forms.IntegerField(
        label="Examiner Number",
        required=True,
        widget=forms.NumberInput,
    )

    first_name = forms.CharField(
        label="First Name",
        max_length=128,
        required=True,
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=128,
        required=True,
    )

    email = forms.EmailField(
        label="Email",
        max_length=128,
        required=True,
    )

    department = forms.ChoiceField(
        label="Department",
        choices=DEPARTMENTS,
    )

    password1 = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + (
            'examiner_number',
            'first_name',
            'last_name',
            'email',
            'department',
        )



class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']