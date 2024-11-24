from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate,login
from student_managment_app.models import CustomeUser,Staffs,Students,AdminHOD
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request,'home.html')
def contact(request):
    return render(request,'contact.html')
def loginUser(request):
    return render(request,'login_page.html')
def doLogin(request):
    email_id=request.GET.get('email')
    password=request.GET.get('password')
    # user_type=request.GET.get('user_type')
    print(email_id)
    if not(email_id and password):
        messages.error(request,'Please provide all the details!!!')
        return render(request,'login_page.html')
    user=CustomeUser.objects.filter(email=email_id,password=password)
    print(user)
    if not user:
        messages.error(request,'Invalid Login Credentials!!!')
        return render(request,'login_page.html')
    login(request,user)
    if(user.user_type==CustomeUser.STUDENT):
        return redirect('student_home/')
    if(user.user_type==CustomeUser.HOD):
        return redirect('admin_home/')
    return render(request,'home.html')
def registration(request):
    return render(request,'registration.html')
def doRegistration(request):
    user_name=request.GET.get('user_name')
    first_name=request.GET.get('first_name')
    last_name=request.GET.get('last_name')
    email_id=request.GET.get('email')
    print(email_id)
    password=request.GET.get('password')
    print(password)
    confirm_password=request.GET.get('confirmPassword')
    if not (email_id and password and confirm_password):
        messages.error(request,'Please provide all the details!!!')
        return render(request,'registration.html')
    if (password!=confirm_password):
        messages.error(request,'Password and Confirm Password must be same!!!')
        return render(request,'registration.html')
    is_user_exists=CustomeUser.objects.filter(email=email_id).exists()
    if is_user_exists:
        messages.error(request,"User email_id already exist!!!")
        return render(request,'registration.html')
    user_type=get_user_type_from_email(email_id)
    print(user_type)
    if user_type is None:
        messages.error(request,'Please follow valid email Id')
        return render(request,'registration.html')
    username=email_id.split('@')[0].split('.')[0]
    if(CustomeUser.objects.filter(username=username).exists()):
        messages.error(request,'User with this username already exists')
        return render(request,'registration.html')
    # user=user_name
    
    user_name.email=email_id
    user_name.password=password
    user_name.user_type=user_type
    user_name.first_name=first_name
    user_name.last_name=last_name
    user_name.save()
    
def get_user_type_from_email(email_id):
    try:
        email_id=email_id
        return email_id
    except:
        return None
    