from django.contrib import admin
from django.urls import path,include
from student_managment_app.views import *
# from student_managment_app import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"), 
	path('contact', contact, name="contact"), 
	path('login', loginUser, name="login"), 
	# path('logout_user', logout_user, name="logout_user"), 
	path('registration', registration, name="registration"), 
	path('doLogin', doLogin, name="doLogin"), 
	path('doRegistration', doRegistration, name="doRegistration"), 
    path('',include('student_managment_app.urls')),
]
