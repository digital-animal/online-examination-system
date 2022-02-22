from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.db import connection
import cx_Oracle

from django.forms import Form
from .forms import QuestionForm, ChoiceForm
from .models import Question, Choice
import re
from django.template import backends

from django.contrib.auth.decorators import login_required

from app_user.models import Student, Examiner

from django.forms import (
    ModelForm,
    modelformset_factory,
    formset_factory,
)

import json

# Create your views here.
def get_lastest_record():
    connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
    cursor = connection.cursor()

    query = """
        SELECT QUESTION_ID 
        FROM QUESTION
        ORDER BY QUESTION_ID DESC
    """

    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    question_id = result[0]

    return question_id


def index(request):


    template_name = 'app_exam/index.html'
    context = {
        'text': "Online Examination System",
        'title': "Exam Homepage"
    }
    return render(request, template_name, context)


######################################################################################
####################################### Basic CRUD ###################################
######################################################################################



######################################################################################
#################################### CREATE ##########################################
######################################################################################
@login_required(login_url='login')
def add_question(request):
    request_examiner = Examiner.objects.filter(examiner_id=request.user.id).first()
    request_student = Student.objects.filter(student_id=request.user.id).first()

    if request_examiner is not None:
        if request.method == 'POST':

            question_form = QuestionForm(request.POST)

            if question_form.is_valid():

                question_text = question_form.cleaned_data.get('question_text')
                course = question_form.cleaned_data.get('course')
                course_id = re.search(r'\d+', str(course)).group(0)
                examiner_id = request.user.id

                connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
                cursor = connection.cursor()

                question_sql = """
                    INSERT INTO QUESTION (QUESTION_TEXT, COURSE_ID, EXAMINER_ID) 
                    VALUES (:question_text, :course_id, :examiner_id)
                """
                
                cursor.execute(question_sql, [question_text, course_id, examiner_id])
                connection.commit()
                cursor.close()

                return redirect('add_choice')

            else:
                raise ValueError('Invalid Form Input')

        else:
            question_form = QuestionForm()
        
        template_name = 'app_exam/add_question.html'
        context = {
            'question_form': question_form,
        }
        return render(request, template_name, context)
    else:
        return HttpResponseRedirect("You are not authorized to view or edit this page")


@login_required(login_url='login')
def add_choice(request):

    #  quering latest inserted row

    connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
    cursor = connection.cursor()
    query = """
        SELECT * FROM QUESTION
        WHERE QUESTION_ID = (
            SELECT MAX(QUESTION_ID)
            FROM QUESTION
        )
    """

    cursor.execute(query)
    output = cursor.fetchone()
    cursor.close()

    question_id = output[0]
    question_text = output[1]

    # request_examiner = Examiner.objects.filter(examiner_id=request.user.id).first()
    # request_student = Student.objects.filter(student_id=request.user.id).first()

    ChoiceFormSet = formset_factory(ChoiceForm, extra=4, max_num=4) # formset class

    if request.method == 'POST':

        formset = ChoiceFormSet(request.POST) # formset object

        if formset.is_valid():

            connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
            cursor = connection.cursor()

            for form in formset:

                choice_text = form.cleaned_data.get('choice_text')
                is_correct = form.cleaned_data.get('is_correct')

                choice_sql = """
                    INSERT INTO CHOICE (CHOICE_TEXT, IS_CORRECT, QUESTION_ID) 
                    VALUES (:choice_text, :is_correct, :question_id)
                """
                
                cursor.execute(choice_sql, [choice_text, is_correct, question_id])
                connection.commit()
                
            cursor.close()

            return redirect('add_question_done')

        else:
            return HttpResponseRedirect('Invalid Form Input')

    else:
        formset = ChoiceFormSet()
    
    template_name = 'app_exam/add_choice.html'
    context = {
        'formset': formset,
        'question_id': question_id,
        'question_text': question_text,
    }
    return render(request, template_name, context)
        


@login_required(login_url='login')
def add_question_done(request):

    template_name = 'app_exam/add_question_done.html'
    context = {
        'message': "Question Saved Successfully",
    }
    return render(request, template_name, context)



########################################################################################
#################################### RETRIEVE ##########################################
########################################################################################

@login_required(login_url='login')
def query_question(request):
    connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
    cursor = connection.cursor()

    course_sql = """
        SELECT COURSE_ID, COURSE_CODE 
        FROM COURSE
    """

    cursor.execute(course_sql)
    courses = cursor.fetchall()
    cursor.close()

    course_dict = {}

    for record in courses:
        course_id = record[0]
        course_code = record[1]
        course_dict[course_id] = course_code
    
    request_examiner = Examiner.objects.filter(examiner_id=request.user.id).first()
    request_student = Student.objects.filter(student_id=request.user.id).first()

    if request_examiner is not None:

        if request.method == 'POST':

            examiner_id = request.user.id
            course_id = request.POST.get('course')

            return redirect('show_question', course_id, examiner_id)

        template_name = 'app_exam/query_question.html'
        context = {
            'course_dict': course_dict,
            'course_id': course_id,
        }
        return render(request, template_name, context)
    else:
        return HttpResponseRedirect("You are not authorized to view this page")


@login_required(login_url='login')    
def show_question(request, course_id, examiner_id):

    connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
    cursor = connection.cursor()

    # retrieving questions
    sql = """
        SELECT *
        FROM QUESTION
        WHERE COURSE_ID = :course_id
        AND EXAMINER_ID = :examiner_id
    """
    print(sql)

    cursor.execute(sql, [course_id, examiner_id])
    question_queryset = cursor.fetchall()
    cursor.close()

    question_list = []

    # passing questions to template
    for record in question_queryset:
        question_id = record[0]
        question_text = record[1]

        connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
        cursor = connection.cursor()

        # retrieving questions
        sql = """
            SELECT *
            FROM CHOICE
            WHERE QUESTION_ID = :question_id
        """
        print(sql)

        cursor.execute(sql, [question_id])
        choice_queryset = cursor.fetchall()

        question_choice_dict = {}

        question_choice_dict['question_id'] = question_id
        question_choice_dict['question_text'] = question_text

        if len(choice_queryset) != 0:
            
            i = 1
            for record in choice_queryset:
                choice_text = record[1]
                choice_index = f'choice_{i}'
                i = i + 1
                question_choice_dict[choice_index] = choice_text

        question_list.append(question_choice_dict)

        cursor.close()

    template_name = 'app_exam/show_question.html'
    context = {
        'question_list': question_list,
        'course_id': course_id,
    }

    return render(request, template_name, context)
 


######################################################################################
#################################### UPDATE ##########################################
######################################################################################


@login_required(login_url='login')
def edit_question(request, question_id):

    question = get_object_or_404(Question, question_id=question_id)

    if request.method == 'POST':

        question_form = QuestionForm(request.POST)

        if question_form.is_valid():

            question_text = question_form.cleaned_data.get('question_text')
            examiner_id = request.user.id

            connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
            cursor = connection.cursor()

            question_sql = """
                UPDATE QUESTION
                SET QUESTION_TEXT = :question_text   
                WHERE QUESTION_ID = :question_id
                AND EXAMINER_ID = :examiner_id
            """
            
            cursor.execute(question_sql, [question_text, question_id, examiner_id])
            connection.commit()
            cursor.close()

                
            request.session['question_id'] = question_id
            request.session['question_text'] = question_text

            return redirect('edit_choice')
    
    else:
        question_form = QuestionForm(instance=question)

    template_name = 'app_exam/edit_question.html'
    context = {
        'question_form': question_form,
        'question_id': question_id,
    }
    return render(request, template_name, context)



@login_required(login_url='login')
def edit_choice(request):

    # quering latest inserted row

    question_id = request.session['question_id']
    question_text = request.session['question_text']

    choice = Choice.objects.filter(question_id=question_id)

    # request_examiner = Examiner.objects.filter(examiner_id=request.user.id).first()
    # request_student = Student.objects.filter(student_id=request.user.id).first()

    # ChoiceFormSet = formset_factory(ChoiceForm) # formset class
    ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm, extra=4, max_num=4) # model formset class

    if request.method == 'POST':

        formset = ChoiceFormSet(request.POST) # formset object

        if formset.is_valid():

            for form in formset:
                connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
                cursor = connection.cursor()

                choice_text = form.cleaned_data.get('choice_text')
                is_correct = form.cleaned_data.get('is_correct')

                choice_sql = """
                    UPDATE 
                        CHOICE
                    SET 
                        CHOICE_TEXT = :choice_text,   
                        IS_CORRECT = :is_correct   
                    WHERE QUESTION_ID = :question_id
                """
                
                cursor.execute(choice_sql, [choice_text, is_correct, question_id])
                connection.commit()
                cursor.close()

            return redirect('edit_question_done')

        else:
            raise ValueError('Invalid Form Input')

    else:
        formset = ChoiceFormSet(queryset=choice)
    
    template_name = 'app_exam/edit_choice.html'
    context = {
        'formset': formset,
        'question_id': question_id,
        'question_text': question_text,
    }
    return render(request, template_name, context)


def edit_question_done(request):

    template_name = 'app_exam/edit_question_done.html'
    context = {
        'message': "Question Updated Successfully",
    }
    return render(request, template_name, context)



######################################################################################
#################################### DELETE ##########################################
######################################################################################

@login_required(login_url='login')
def delete_question(request, question_id):

    current_examiner = Examiner.objects.filter(examiner_id=request.user.id).first()
    current_student = Student.objects.filter(student_id=request.user.id).first()

    if current_examiner is not None:

        examiner_id = request.user.id
        if request.method == 'POST':
            
            connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
            cursor = connection.cursor()
            sql_permission = "SELECT EXAMINER_ID FROM QUESTION WHERE QUESTION_ID = :question_id"
            
            cursor.execute(sql_permission, [question_id])
            authorized_examiner = cursor.fetchone()[0]
            # print(f"Authorized Examiner = {authorized_examiner}\n\n\n")

            cursor.close()

            # finally delete
            if examiner_id == authorized_examiner:
                
                connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
                cursor = connection.cursor()

                sql = """
                    DELETE
                    FROM QUESTION
                    WHERE QUESTION_ID = :question_id
                    AND EXAMINER_ID = :examiner_id
                """

                cursor.execute(sql, [question_id, examiner_id])
                connection.commit()
                cursor.close()

                return redirect('delete_question_done')

            else:
                return HttpResponse("You are not authorized to delete any question")

        template_name = 'app_exam/delete_question.html'
        context = {
            # 'request_examiner': current_examiner,
            'request_examiner': examiner_id,
            'question_id': question_id,
        }
        return render(request, template_name, context)

    else:
        return HttpResponseRedirect("You are not authorized to view or edit this page")



def delete_question_done(request):

    template_name = 'app_exam/delete_question_done.html'
    context = {
        'message': "Question Deleted Successfully",
    }
    return render(request, template_name, context)


#########################################################################
################################# EXAM PART #############################
#########################################################################

@login_required(login_url='login')
def create_exam(request):

    connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
    cursor = connection.cursor()

    sql = """SELECT COURSE_ID, COURSE_CODE FROM COURSE"""

    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    course_dict = {}

    for record in result:
        course_id = record[0]
        course_code = record[1]

        course_dict[course_id] = course_code

    template_name = 'app_exam/create_exam.html'
    context = {
        'course_dict': course_dict,
    }

    request_examiner = Examiner.objects.filter(examiner_id=request.user.id).first()
    request_student = Student.objects.filter(student_id=request.user.id).first()

    if request_student is not None:

        if request.method == 'POST':
            course_id = request.POST.get('course')
            marks = request.POST.get('marks')

            return redirect('mcq', course_id, marks)

        return render(request, template_name, context)

    else:
        return HttpResponseRedirect("You are not authorized to view or edit this page")


@login_required(login_url='login')
def mcq(request, course_id, marks):

    connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
    cursor = connection.cursor()

    question_list = []

    sql = """
        SELECT *
        FROM QUESTION
        WHERE COURSE_ID = :course_id
        ORDER BY QUESTION_ID
    """

    sql = """
        SELECT *
        FROM QUESTION
        WHERE COURSE_ID = :course_id
        ORDER BY dbms_random.value
    """

    # sql = """
    #     SELECT *
    #     FROM (
    #         SELECT *
    #         FROM QUESTION
    #         WHERE COURSE_ID = :course_id
    #     ORDER BY DBMS_RANDOM.RANDOM )    
    #     FETCH FIRST :count ROWS ONLY
    # """

    # sql = """
    #     SELECT * 
    #     FROM QUESTION 
    #     SAMPLE(20) 
    #     WHERE COURSE_ID = :course_id 
    #     FETCH FIRST :count ROWS ONLY
    # """

    print(sql)
    
    # cursor.execute(sql, [course_id, marks])

    cursor.execute(sql, [course_id])
    question_queryset = cursor.fetchall()
    cursor.close()

    print(question_queryset)

    question_choice_dict = {}
    
    # passing questions to template
    for record in question_queryset:
        print(record)
        print(record[0])
        print("\n\n\n")
        question_id = record[0]
        question_text = record[1]

        question_dict = {
            'question_id' : question_id,
            'question_text' : question_text,
        }

        # fetching choices for corresponding question
        connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
        cursor = connection.cursor()
        choice_sql = """
            SELECT *
            FROM CHOICE
            WHERE QUESTION_ID = :question_id
        """
        # print(choice_sql)
        cursor.execute(choice_sql, [question_id])
        choice_queryset = cursor.fetchall()
        cursor.close()


        index = 1
        for result in choice_queryset:

            choice_id = result[0]
            choice_text = result[1]
            choice_index = f'choice_{index}'
            index = index + 1

            question_dict[choice_index] = {
                'choice_id': choice_id,
                'choice_text': choice_text,
            }

        if len(question_dict) == 6: 
            question_list.append(question_dict)

        if len(question_list) == marks:
            break

    print(json.dumps(question_list, indent=4, sort_keys=True))
    


    # save_exam(request, *question_list)

    template_name = 'app_exam/mcq.html'
    context = {
        'question_list': question_list,
        'course_id': course_id,
        'full_marks': marks,
    }

    return render(request, template_name, context)

def save_exam(request, *args, **kwargs):
    if args:
        print(json.dumps(args, indent=4, sort_keys=True))

    if kwargs:
        print(kwargs)
    
    template_name = ""
    context = {}
    return render(redirect, template_name, context)


@login_required(login_url='login')
def result(request):

    ans_dict = {}
    ans_list = []
    marks = 0

    template_name = 'app_exam/result.html'
    context = {
        'message': 'Answers accepted. Wait for the evaluation.',
    }

    # fetching submitted answers from template
    if request.method == 'POST':
        queryDict = request.POST

        for key, value in queryDict.items():
            if key != "csrfmiddlewaretoken":
                selected_question_id = key
                selected_choice_id = value

                connection = cx_Oracle.connect("dj/dj@localhost:1521/orclpdb", encoding="UTF-8")
                cursor = connection.cursor()

                print((selected_question_id, selected_choice_id))
                sql = """
                    SELECT IS_CORRECT 
                    FROM CHOICE
                    WHERE QUESTION_ID = :selected_question_id 
                    AND CHOICE_ID = :selected_choice_id
                """
                print(sql)

                cursor.execute(sql, [selected_question_id, selected_choice_id])
                result = cursor.fetchone()
                is_correct = result[0]
                if  is_correct == 1:
                    marks = int(marks) + 1
                    
                cursor.close()

    print(marks)

    context['marks'] = marks

    print(context)

    return render(request, template_name, context)


