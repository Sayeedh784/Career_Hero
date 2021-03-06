from operator import mod
from statistics import mode
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# Create your models here.
class User(AbstractUser):
  is_counselor= models.BooleanField(default=False)
  is_student = models.BooleanField(default=False)

CATEGORIES= (
  ('School Level','School Level'),
  ('College Level','college Level'),
  ('University Level','University Level'),
)

class Counselor(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
  name=models.CharField(max_length=30,blank=True,null=True)
  email = models.EmailField(max_length=40,blank=True,null=True)
  mobile = models.IntegerField(blank=True,null=True)
  image = models.ImageField(upload_to='images/',null=True,blank=True)
  designation = models.CharField(max_length=30,blank=True,null=True)
  institute = models.CharField(max_length=300,blank=True,null=True)
  category = models.CharField(max_length=50,choices=CATEGORIES,null=True,blank=True)
  address = models.CharField(max_length=100,blank=True,null=True)
  counselling_experience = models.IntegerField(blank=True,null=True)
  description = models.TextField(max_length=2000,blank=True,null=True)
  per_session_fee = models.IntegerField(blank=True,null=True)
  counselling_day=models.CharField(max_length=100,null=True,blank=True)
  counselling_time=models.CharField(max_length=100,null=True,blank=True)

  def __str__(self):
    return str(self.id)

  def get_absolute_url(self):
    return reverse('counselor_profile', args=[str(self.id)])

class Student(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
  name = models.CharField(max_length=30,blank=True,null=True)
  email = models.EmailField(max_length=40,blank=True,null=True)
  mobile = models.IntegerField(blank=True,null=True)
  image = models.ImageField(upload_to='images/',null=True,blank=True)
  cls = models.CharField(max_length=30,blank=True,null=True)
  institute = models.CharField(max_length=300,blank=True,null=True)
  address = models.CharField(max_length=100,blank=True,null=True)
  area_of_interest = models.CharField(max_length=100,blank=True,null=True)

  def __str__(self):
    return str(self.id)

  def get_absolute_url(self):
    return reverse('student_profile', args=[str(self.id)])

class Appoinment(models.Model):
  req_user=models.ForeignKey(Student,on_delete=models.CASCADE,blank=True,null=True)
  accept_user=models.ForeignKey(Counselor,on_delete=models.CASCADE,blank=True,null=True)
  topics = models.CharField(max_length=200,blank=True,null=True)
  appoinment_date=models.DateField()
  appoinment_time = models.TimeField()
  appoinment_status = models.CharField(max_length=20,default="Pending")

  def __str__(self):
    return str(self.id)

class Article(models.Model):
  author = models.ForeignKey(Counselor,on_delete=models.CASCADE)
  title = models.CharField(max_length=70)
  body = models.TextField()
  image = models.ImageField(upload_to='images',)
  date = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ['-date',]
    
  def __str__(self):
    return str(self.id)

  def get_absolute_url(self):
    return reverse('article_detail', args=[str(self.id)])

class ThreadModel(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
  receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')

class MessageModel(models.Model):
  thread = models.ForeignKey(ThreadModel,related_name='+',
  on_delete=models.CASCADE,blank=True,null=True)
  sender_user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
  receiver_user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
  body = models.CharField(max_length=1000)
  image = models.ImageField(upload_to='message_images/',blank=True,null=True)
  date = models.DateTimeField(auto_now_add=True)
  is_read= models.BooleanField(default=False)