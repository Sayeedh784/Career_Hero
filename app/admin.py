from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ['id','username','email']
@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
  list_display = ['id','name','designation','category']
  
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  list_display = ['id','name','cls','area_of_interest']
  
@admin.register(Appoinment)
class AppoinmentAdmin(admin.ModelAdmin):
  list_display = ['id','req_user','accept_user','appoinment_time','appoinment_date']
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
  list_display = ['id','title','author','date']

@admin.register(ThreadModel)
class ThreadModelAdmin(admin.ModelAdmin):
  list_display=['id','user','receiver']

@admin.register(MessageModel)
class MessageModelAdmin(admin.ModelAdmin):
  list_display=['id','sender_user','receiver_user','date']