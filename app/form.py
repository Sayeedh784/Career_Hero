from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import *
from django.forms import NumberInput, fields, widgets
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm, AuthenticationForm, UsernameField
PasswordChangeForm, PasswordResetForm, SetPasswordForm


class CounselorSignupForm(UserCreationForm):
  name = forms.CharField(max_length=30)
  email=forms.EmailField(max_length=50)
  mobile = forms.IntegerField()
  designation = forms.CharField(max_length=20)
  institute = forms.CharField(max_length=100)

  class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','name', 'email','mobile','designation','institute', 'password1', 'password2']
        labels = {'email': 'Email','mobile,':'Mobile','designation':'Designation','institute':'Institute'}
        widgets = {'username': forms.TextInput(
            attrs={'class': "form-control"})}
    
  @transaction.atomic
  def save(self):
      user = super().save(commit=False)
      user.is_counselor = True
      user.save()

      counselor = Counselor.objects.create(user=user)
      counselor.name = self.cleaned_data.get('name')
      counselor.email = self.cleaned_data.get('email')
      counselor.mobile = self.cleaned_data.get('mobile')
      counselor.designation = self.cleaned_data.get('designation')
      counselor.institute = self.cleaned_data.get('institute')
      counselor.save()
      return user

class StudentSignupForm(UserCreationForm):
  name = forms.CharField(max_length=30)
  email=forms.EmailField(max_length=50)
  mobile = forms.CharField()
  cls = forms.CharField(max_length=50)
  institute = forms.CharField(max_length=100)

  class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','name', 'email','mobile','cls','institute', 'password1', 'password2']
        labels = {'email': 'Email','mobile,':'Mobile','cls':'Class','institute':'Institute'}
        widgets = {'username': forms.TextInput(
            attrs={'class': "form-control",})}
    
  @transaction.atomic
  def save(self):
      user = super().save(commit=False)
      user.is_student = True
      user.save()

      student = Student.objects.create(user=user)
      student.name = self.cleaned_data.get('name')
      student.email = self.cleaned_data.get('email')
      student.mobile = self.cleaned_data.get('mobile')
      student.cls = self.cleaned_data.get('cls')
      student.institute = self.cleaned_data.get('institute')
      student.save()
      return user

class StudentUpdateForm(forms.ModelForm):
  class Meta:
    model = Student
    fields = ('name', 'mobile', 'email', 'image','cls','institute','address','area_of_interest' )
    labels = {'cls':'Class'}


class AppoinmentForm(forms.ModelForm):
  appoinment_time= forms.TimeField(widget=NumberInput(attrs={'type': 'time'}))
  appoinment_date=forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
  class Meta:
    model = Appoinment
    fields=('topics','appoinment_time','appoinment_date')

class PostForm(forms.ModelForm):
  class Meta:
    model = Article
    fields= ('title','body','image')


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100,)


class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)



class MyPasswordChangeForm(PasswordChangeForm):
  old_password = forms.CharField(label=_("Old Password"),
  strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,
 'class': 'form-control'}))
  new_password1 = forms.CharField(label=_("New Password"),
  strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'New password',
  'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
  new_password2 = forms.CharField(label=_("Confirm New Password"),
  strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
  'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
  email  = forms.EmailField(label=_("Email"),max_length=254,
  widget=forms.EmailInput(attrs={'autocomplete':'email',
  'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
  new_password1= forms.CharField(label=_("New Password"),
  strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
  'class':'form-control'}),help_text=password_validation.
  password_validators_help_text_html())
  new_password2= forms.CharField(label=_("Comfrim New Password"),
  strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
  'class':'form-control'}))

