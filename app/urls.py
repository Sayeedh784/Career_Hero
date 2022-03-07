from django.urls import path
from .import views
from .views import *
from .form import *
from django.contrib.auth import views as auth_views

urlpatterns=[
  path('',views.home,name="home"),
  path('register/',views.register,name="register"),
  path('couselor_signup/',views.Counselor_register.as_view(),name="counselor_signup"),
  path('student_signup/',views.Student_register.as_view(),name="student_signup"),

  path('profile/<int:pk>/',views.profile,name="profile"),
  path('counselor_form/<int:pk>/',views.CounselorUpdateView.as_view(),name="counselor_form"),
  path('student_form/<int:pk>/',views.StudentUpdateView.as_view(),name="student_form"),
  path('counselor_profile/<int:pk>/',views.counselor_profile,name="counselor_profile"),
  path('student_profile/<int:pk>/',views.student_profile,name="student_profile"),

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