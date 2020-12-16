from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.core import validators
import datetime

YEARS = [x for x in range(2000, 3000)]




class UserForm(UserCreationForm):
    password1 = forms.CharField(
        min_length=8, max_length=30, widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']
        help_texts = {
            'username': '''Same as Your <strong>USN</strong> in <strong>UPPER</strong> case'''
        }
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'})

        }
        def clean_username(self):
            return self.cleaned_data['username'].upper()


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'student_name',
            'USN',
            'student_mbl_no',
            'adress',
            'father_name',
            'father_mbl_no',
            'Branch',
            'dob',
            'gender']


class SelectionForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['room']


class DuesForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Student.objects.all().filter(no_dues=True))


class NoDuesForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Student.objects.all().filter(no_dues=False))


class DateInput(forms.DateInput):
    input_type = 'date'


class LeaveForm(forms.ModelForm):
    start_date = forms.DateField(
        initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))
    end_date = forms.DateField(
        initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))
    reason = forms.CharField(max_length=100, help_text='100 characters max.',
                             widget=forms.TextInput(attrs={'placeholder': 'Enter Reason here'}))

    class Meta:
        model = Leave
        fields = [
            'start_date',
            'end_date',
            'reason']


class RepairForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['repair']



