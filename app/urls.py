from django.urls import path
from .import views
from .views import *
from .form import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
  path('',views.home,name="home"),
  path('register/',views.register,name="register"),
  path('couselor_signup/',views.counselor_register,name="counselor_signup"),
  path('student_signup/',views.student_register,name="student_signup"),
  path('search_list/',views.search_list,name="search_list"),

  path('profile/<int:pk>/',views.profile,name="profile"),
  path('counselor_form/<int:pk>/',views.CounselorUpdateView.as_view(),name="counselor_form"),
  path('student_form/<int:pk>/',views.StudentUpdateView.as_view(),name="student_form"),
  path('counselor_profile/<int:pk>/',views.counselor_profile,name="counselor_profile"),
  path('counselor/',views.counselor,name="counselor"),
  path('student_profile/<int:pk>/',views.student_profile,name="student_profile"),

  path('appoinmentForm/<int:pk>/',views.appointment_form,name="appoinmentForm"),
  path('appoinment/',views.appoinment,name="appointment"),
#   path('student_appoinment/',views.student_appoinment,name="student_appoinment"),

  path('cancel/<int:pk>/',views.cancelRequest,name="cancel"),
  path('decline/<int:pk>/',views.decline,name="decline"),
  path('accept/<int:pk>/',views.accept,name="accept"),


  #article
  path('article_edit/<int:pk>/',ArticleUpdateView.as_view(), name='article_edit'),
  path('article_detail/<int:pk>/',ArticleDetailView.as_view(), name='article_detail'),
  path('article_delete/<int:pk>/',ArticleDeleteView.as_view(), name='article_delete'),
  path('article_new/', views.create_post, name='article_new'), 
  path('article_list/', ArticleListView.as_view(), name='article_list'),

#Message
  path('inbox/', ListThreads.as_view(), name='inbox'),
  path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
  path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
  path('inbox/<int:pk>/create-message/',CreateMessage.as_view(), name='create-message'),

  path('login/',views.login_request, name='login'),
  path('logout/',views.logout_view, name='logout'),
  path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,
  success_url='/passwordchangedone/'), name='passwordchange'),
  path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),
        name='passwordchangedone'),
        
  path('password-reset/', auth_views.PasswordResetView.
        as_view(template_name='app/password_reset.html',
                form_class=MyPasswordResetForm), name='password_reset'),

  path('password-reset/done/', auth_views.PasswordResetDoneView.
        as_view(template_name='app/password_reset_done.html'),
        name='password_reset_done'),

  path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.
        as_view(template_name='app/password_reset_confirm.html',
                form_class=MySetPasswordForm),
        name='password_reset_confirm'),

  path('password-reset-complete/', auth_views.PasswordResetCompleteView.
        as_view(template_name='app/password_reset_complete.html'),
        name='password_reset_complete'),
] 