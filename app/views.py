from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import *
from django.contrib import messages
from .form import *
from django.contrib.auth import login, logout,authenticate
from django.views.generic import CreateView,ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
# Create your views here.


def home(request):
  return render(request, 'app/home.html')

def register(request):
  return render(request, 'app/register.html')

class Counselor_register(View):
  def get(self, request):
    form = CounselorSignupForm()
    return render(request, 'app/counselorsignup.html', {'form': form})

  def post(self, request):
    form = CounselorSignupForm(request.POST)
    if form.is_valid():
      messages.success(request, "Congratulations!!! Registered successfully")
      form.save()
    return redirect('/login')

class Student_register(View):
  def get(self, request):
    form = StudentSignupForm()
    return render(request, 'app/studentsignup.html', {'form': form})

  def post(self, request):
    form = StudentSignupForm(request.POST)
    if form.is_valid():
      messages.success(request, "Congratulations!!! Registered successfully")
      form.save()
    return redirect('/login')

def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'app/login.html',context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/login')


def profile(request,pk):
  if request.user.is_counselor:
    counselor= Counselor.objects.get(user_id=request.user.id)
    context ={'counselor':counselor}
    return render(request, 'app/counselorProfile.html',context)
  elif request.user.is_student:
    student= Student.objects.get(user_id=request.user.id)
    context ={'student':student}
    return render(request, 'app/studentProfile.html',context)



#counselor
class CounselorUpdateView(LoginRequiredMixin, UpdateView):
  model = Counselor
  fields = ('name', 'mobile', 'email', 'image','designation','institute','category','address','counselling_experience','description','per_session_fee' )
  template_name = 'app/updateForm.html'
  login_url = 'login'

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request, *args, **kwargs)

def counselor_profile(request,pk):
  counselor = Counselor.objects.get(pk=pk)
  context = {'counselor':counselor}
  return render(request, 'app/counselorProfile.html',context)

def counselor(request):
  counselor = Counselor.objects.all()
  context={'counselors':counselor}
  return render(request, 'app/counselor.html',context)

#student
def student_profile(request,pk):
  student = Student.objects.get(pk=pk)
  context = {'student':student}
  return render(request, 'app/studentProfile.html',context)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
  model = Student
  fields = ('name', 'mobile', 'email', 'image','cls','institute','address','area_of_interest' )
  template_name = 'app/updateForm.html'
  login_url = 'login'

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request, *args, **kwargs)


#Appoinment
def appointment_form(request,pk):
  print(request.POST)
  if request.method == 'POST':
    form = AppoinmentForm(request.POST)
    if form.is_valid():
      form.instance.accept_user = Counselor.objects.get(pk=pk)
      instance = form.save(commit=False)
      form.instance.req_user = Student.objects.get(user_id=request.user.pk)
      instance.save()
      messages.success(request, 'Congratulations, Your request sent succesfully!!!')
      
  else:
    form =AppoinmentForm()
  context = {'form':form,}
  return render(request,'app/appoinmentForm.html',context)

def appoinment(request):
  if request.user.is_student:
    stu_apn = Appoinment.objects.all()
    return render(request, 'app/appoinments.html',{'stu_apn':stu_apn})
  elif request.user.is_counselor:
    counselor_apn=Appoinment.objects.all()
    student=Student.objects.all()
    return render(request, 'app/counselor_appoinment.html',{'counselor_apn':counselor_apn,'student':student})


#appoinment status

def cancelRequest(request,pk):
  url=request.META.get('HTTP_REFERER')
  apn = get_object_or_404(Appoinment, id=pk)
  apn.delete()
  return redirect(url)
  

def decline(request,pk):
  url=request.META.get('HTTP_REFERER')
  apn = get_object_or_404(Appoinment, pk=pk)
  apn.appoinment_status = "Decline"
  apn.save()
  return redirect(url)
  # return render(request, 'app/request.html',{'apn':apn})

def accept(request,pk):
  url=request.META.get('HTTP_REFERER')
  apn = get_object_or_404(Appoinment, pk=pk)
  apn.appoinment_status = "Accepted"
  apn.save()
  return redirect(url)
  # return render(request, 'app/request.html',{'apn':apn})