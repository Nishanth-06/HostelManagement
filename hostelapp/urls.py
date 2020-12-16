from django.urls import path
from .views import *


app_name = 'hostelapp'

urlpatterns = [
    path('',homepage,name='homepage'),
    path('signup/',student_registration,name='signup'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('student_profile/',student_profile,name='student_profile'),
    path('after_reg/',student_after_registration,name='after_reg'),
    path('Room_maintenence/',maintainence,name='Room_maintenence'),
    path('warden_home/',warden_homepage,name='warden_home'),
    path('room_select/',select,name='room_select'),
    path('leave/',user_leave,name='leave'),

]
