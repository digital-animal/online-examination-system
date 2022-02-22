from django import forms
from django.forms import ModelForm

from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        label="Question",
        max_length=1024,
        required=True,
        widget=forms.Textarea(attrs={'id': 'question'}),
    )

    class Meta:
        model = Question
        fields = [
            'course',
            'question_text',
        ]

class ChoiceForm(forms.ModelForm):
    choice_text = forms.CharField(
        label = "",
        max_length=256,
        required=False,
    )

    is_correct = forms.IntegerField(
        required=True,
        widget=forms.NumberInput,
    )

    class Meta:
        model = Choice
        fields = [
            # 'question',
            'choice_text',
            'is_correct',
        ]
        
