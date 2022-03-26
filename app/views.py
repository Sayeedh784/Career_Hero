import email
from itertools import chain
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from .models import *
from django.contrib import messages
from django.db.models import Q
from .form import *
from django.core.paginator import Paginator
from django.contrib.auth import login, logout,authenticate
from django.views.generic import CreateView,ListView,DetailView,DeleteView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.

#Search 

def search_list(request):
  if request.method == 'POST':
    q = request.POST['q']
    counselor_data = Counselor.objects.filter(name__icontains=q)
    data = chain(counselor_data)
    total_counsellor=counselor_data.count()
  context = {'data': data, 'q': q, 'counselor_data':counselor_data,'total_counsellor':total_counsellor}
  return render(request,'app/search_list.html',context)


def home(request):
  article = Article.objects.all()
  recent_article=article[:3]
  counselor = Counselor.objects.all()
  return render(request, 'app/home.html',{'recent_article':recent_article,'counselors':counselor})

def register(request):
  return render(request, 'app/register.html')


def counselor_register(request):
  if request.method == "POST":
    form=CounselorSignupForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request,f'Account Created for {username}!!')
      form = CounselorSignupForm()
      return redirect('login')
  else: 
    form = CounselorSignupForm()
  context = {
    'form':form
  }
  return render(request,'app/counselorsignup.html',context)

def student_register(request):
  if request.method == "POST":
    form=StudentSignupForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request,f'Account Created for {username}!!')
      form = StudentSignupForm()
      return redirect('login')
  else: 
    form = StudentSignupForm()
  context = {
    'form':form
  }
  return render(request,'app/studentsignup.html',context)


def login_request(request):
    next_url = request.GET.get('next')
    print(next_url)
    if request.method =='POST':
        next_url = request.POST.get('next')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                if next_url:
                    return redirect(next_url)
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
    articles = Article.objects.filter(author_id=Counselor.objects.get(user_id=request.user.id))
    context ={'counselor':counselor,'articles':articles}
    return render(request, 'app/counselorProfile.html',context)
  elif request.user.is_student:
    student= Student.objects.get(user_id=request.user.id)
    context ={'student':student}
    return render(request, 'app/studentProfile.html',context)



#counselor
class CounselorUpdateView(LoginRequiredMixin, UpdateView):
  model = Counselor
  fields = ('name', 'mobile', 'email', 'image','designation','institute','category','address','counselling_experience','description','per_session_fee','counselling_day','counselling_time' )
  template_name = 'app/updateForm.html'
  login_url = 'login'

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request, *args, **kwargs)

def counselor_profile(request,pk):
  counselor = Counselor.objects.get(pk=pk)
  thread = ThreadModel.objects.filter(pk=pk)
  message_list = MessageModel.objects.filter(thread__pk__contains=pk)
  # articles = Article.objects.filter(author_id=request.user.id)
  context = {'counselor':counselor,'thread':thread,'message_list':message_list,}
  return render(request, 'app/counselorProfile.html',context)

def counselor(request):
  counselor = Counselor.objects.all()
  total_counsellor = counselor.count()
  page = Paginator(counselor,per_page=4)
  page_list=request.GET.get('page')
  page=page.get_page(page_list)
  context={'counselors':counselor,'total_counsellor':total_counsellor,'page':page}
  return render(request, 'app/counselor.html',context)

#student
def student_profile(request,pk):
  student = Student.objects.get(pk=pk)
  thread = ThreadModel.objects.filter(pk=pk)
  message_list = MessageModel.objects.filter(thread__pk__contains=pk)
  context = {'student':student,'thread':thread,'message_list':message_list}
  return render(request, 'app/studentProfile.html',context)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
  model = Student
  form_class = StudentUpdateForm
  template_name = 'app/updateForm.html'
  login_url = 'login'

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request, *args, **kwargs)


#Appoinment
def appointment_form(request,pk):
  if request.method == 'POST':
    form = AppoinmentForm(request.POST)
    if form.is_valid():
      form.instance.accept_user = Counselor.objects.get(pk=pk)
      instance = form.save(commit=False)
      form.instance.req_user = Student.objects.get(user_id=request.user.pk)
      instance.save()
      current_site=get_current_site(request)
      template=render_to_string('app/account.html',{'domain':current_site.domain})
      email=EmailMessage(
        'Appointment Request',
        template,
        settings.EMAIL_HOST_USER,
        [form.instance.accept_user.email],
      )
      email.fail_silently=False
      email.send()
      return redirect('appointment')
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


def accept(request,pk):
  url=request.META.get('HTTP_REFERER')
  apn = get_object_or_404(Appoinment, pk=pk)
  apn.appoinment_status = "Accepted"
  apn.save()
  return redirect(url)


#Article


@login_required
def create_post(request, pk=None):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.author = Counselor.objects.get(user_id=request.user.pk)
            form.save()
            return redirect('article_list')
    else:
        form = PostForm()
    context = {'form' : form}
    return render(request, 'app/article_new.html', context)


class ArticleListView(ListView):
  model = Article
  template_name = 'app/article_list.html'
  

class ArticleUpdateView(LoginRequiredMixin,UpdateView):
  model = Article
  fields = ('title','body','image')
  template_name = 'app/article_edit.html'
  login_url = 'login'

  def dispatch(self,request,*args,**kwargs):
    obj= self.get_object()
    if obj.author.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request,*args,**kwargs)

class ArticleDetailView(DetailView):
  model = Article
  template_name = 'app/article_detail.html'
  login_url = 'login'

class ArticleDeleteView(LoginRequiredMixin,DeleteView):
  model = Article
  template_name = 'app/article_delete.html'
  success_url = reverse_lazy('article_list')
  login_url = 'login'

  def dispatch(self,request,*args,**kwargs):
    obj= self.get_object()
    if obj.author.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request,*args,**kwargs)


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(
            Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }

        return render(request, 'app/inbox.html', context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'app/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(
                    user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(
                    user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            messages.error(request, 'Invalid username!!')
            return redirect('create-thread')


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'app/thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()

        return redirect('thread', pk=pk)
