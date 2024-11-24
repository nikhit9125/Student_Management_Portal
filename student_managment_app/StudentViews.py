from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import datetime

def student_home(request):
    student_obj=Students.objects.get(admin=request.user_id)
    total_attendence=AttendenceReport.objects.filter(student_id=student_obj).count()
    attendence_present=AttendenceReport.objects.filter(student_id=student_obj,status=True).count()
    attendence_absent=AttendenceReport.objects.filter(student_id=student_obj,status=False).count()
    course_obj=Courses.objects.get(id=student_obj.course_id.id)
    total_subject=Subjects.objects.filter(course_id=course_obj).count()
    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendence=Attendence.objects.filter(subject_id=subject.id)
        attendence_present_count=AttendenceReport.objects.filter(attendence_id__in=attendence,status=True,student_id=student_obj.id).count()
        attendence_absent_count=AttendenceReport.objects.filter(attendence_id__in=attendence,status=False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendence_present_count)
        data_absent.append(attendence_absent_count)
        context={
            'total_attendence':total_attendence,
            'attendence_present':attendence_present,
            'attendence_absent':attendence_absent,
            'total_subject':total_subject,
            'subject_name':subject_name,
            'data_present':data_present,
            'data_absent':data_absent

        }
        return render(request,'student_template/student_home_template.html',context)
def student_view_attendence(request):
    #Getting Logged in Student Data
    student=Students.objects.get(admin=request.user.id)
    #Getting Course Enrolled of Loggedin student
    course=student.course_id
    #Getting the Subjects of Course Enrolled
    subjects=Subjects.objects.filter(course_id=course)
    context={
        'subjects':subjects
    }
    return render(request,'student_template/student_view_attendence.html',context)
def student_view_attendence_post(request):
    if(request.method!='POST'):
        messages.error(request,'Invalid Method')
        return redirect('student_view_attendence')
    else:
        subject_id=request.POST.get('subject')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        #Parshing the date data into python object
        start_date_parse=datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
        end_date_parse=datetime.datetime.strptime(end_date,'%Y-%m-%d').date()

        subject_obj=Subjects.objects.get(id=subject_id)
        user_obj=CustomeUser.objects.get(id=request.user.id)
        stud_obj=Students.objects.get(admin=user_obj)

        attendence=Attendence.objects.filter(attendence_data__range=(start_date_parse,end_date_parse),subject_id=subject_obj)

        attendence_reports=AttendenceReport.objects.filter(attendence_id__in=attendence,subject_id=subject_obj)
        context={
            'subject_obj':subject_obj,
            'attendence_reports':attendence_reports
        }
        return render(request,'student_template/student_attendence_data.html',context)
def student_apply_leave(request):
    studnet_obj=Students.objects.get(admin=request.user.id)
    leave_data=LeaveReportStudent.objects.filter(student_id=studnet_obj)
    context={
        'leave_data':leave_data
    }
    return render(request,'student_template/student_apply_leave.html',context)
def student_apply_leave_save(request):
    if(request.method!='POST'):
        messages.error(request,'Invalid Method')
        return redirect('student_apply_leave')
    else:
        leave_date=request.POST.get('leave_date')
        leave_message=request.POST.get('leave_message')
        student_obj=Students.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_message,leave_status=0)
            leave_report.save()
            messages.success(request,'Application for Leave')
            return redirect('student_apply_leave')
        except:
            messages.error(request,'Failed to Apply Leave')
            return redirect('student_apply_leave')
def student_feedback(request):
    student_obj=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=student_obj)
    context={
        'feedback_data':feedback_data
    }
    return render(request,'student_template/student_feedback.html',context)
def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)
 
        try:
            add_feedback = FeedBackStudent(student_id=student_obj,
                                           feedback=feedback,
                                           feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')
 
 
def student_profile(request):
    user = CustomeUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
 
    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)
def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

 
        try:
            customeuser = CustomeUser.objects.get(id=request.user.id)
            customeuser.first_name = first_name
            customeuser.last_name = last_name
            if password != None and password != "":
                customeuser.set_password(password)
            customeuser.save()
 
            student = Students.objects.get(admin=customeuser.id)
            student.address = address
            student.save()
             
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')
def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    context = {
        "student_result": student_result,
    }
    return render(request, "student_template/student_view_result.html", context)

