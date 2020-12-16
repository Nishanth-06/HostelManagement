from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime,calendar
import datetime
from django.core.exceptions import ObjectDoesNotExist


def homepage(request):
    return render(request,'index.html')


def student_registration(request):
    form = UserForm()
    context = ''
    if request.method=='POST':
        form = UserForm(data=request.POST)


        if form.is_valid():

            data = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.save()
            Student.objects.create(user=new_user)
            form = UserForm
            user = authenticate(
                request,
                username=data['username'],
                password=data['password1']
            )
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("hostelapp:after_reg")
                else:
                    context = 'acc is in active'
            else:
                context = 'Disabled acc'

        else:
            form = UserForm()

    return render(request,'signup.html',{'form':form,'message':context})


@login_required
def student_after_registration(request):
    form = RegistrationForm()
    if request.method=='POST':
        form = RegistrationForm(data=request.POST,instance=request.user.student)
        if form.is_valid():
            form.save()
            return redirect('hostelapp:student_profile')
        else:
            form = RegistrationForm()
    else:
        form = RegistrationForm()
    return render(request,'after_reg.html',{'form':form})

def user_login(request):
    context = ''
    if request.method=='POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(request,username = username,password = password)
        if user is not None:
            if user.is_warden:
                if user.is_active:
                    login(request,user)
                    return redirect('hostelapp:warden_home')

            else:
                if user.is_active:
                    login(request,user)
                    return redirect("hostelapp:student_profile")

        else:
            context = 'Disabled acc contact Your warden or Admin'


    return render(request,'Login.html',{'message':context})



@login_required
def warden_homepage(request):
    user = request.user
    if user is not None:
        if  user.is_warden:
            login(request,user)
            room_list = user.warden.hostel.room_set.all().order_by('no')

        else:
            return HttpResponse("Invalid Login")

    return render(request,'warden_home.html',{'room':room_list})

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'index.html')


@login_required
def student_profile(request):
    context = ''
    user = request.user
    if user is not None:
        if user.is_warden:
            return HttpResponse('Invalid Login')
        if user.is_active:
            login(request, user)
            student = request.user.student
            leaves = Leave.objects.filter(student=request.user.student)
            if not request.user.student.room_allotted:
                context = 'Please Select room'
            return render(request, 'Student_profile.html', {'student': student, 'leaves': leaves,'msg':context})

        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')


@login_required
def select(request):
    form = SelectionForm()
    if request.method=='POST':
        if request.user.student.room:
            old_room_id = request.user.student.room_id
            print(f'old room id:{old_room_id}')
        form = SelectionForm(data=request.POST,instance=request.user.student)
        if form.is_valid():
            if request.user.student.room_id:
                request.user.student.room_allotted = True
                new_room_id = request.user.student.room_id
                print(f'new room id:{new_room_id}')
                room = Room.objects.get(id=new_room_id)
                room.vacant = False
                room.save()
                try:
                    room = Room.objects.get(id=old_room_id)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
                student = form.save()
                return redirect("hostelapp:student_profile")

    return render(request,'room.html',{'form':form})




def user_leave(request):
    form = LeaveForm()
    if request.method =="POST":
        form = LeaveForm(data=request.POST)

        if form.is_valid() and request.user.student.room_allotted:
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            delta = end-start
            if delta.days >0 and (start-datetime.date.today()).days>=0:
                usr_contr = Leave.objects.filter(
                    student=request.user.student,start_date__lte=end,end_date__gte=start
                )
                count = usr_contr.count()
                count = int(count)
                if count ==0:
                    leave_form = form.save(commit=False)
                    student = request.user.student
                    leave_form.student = student
                    leave_form.save()
                    leaves = Leave.objects.filter(student=request.user.student)

                    return render(request, 'Student_profile.html', {'student': student, 'leaves': leaves})
                else:
                    return HttpResponse('<h3>Already have a Leave in this period Try another</h3>  <br> '
                                        '<a href = \'\' style = "text-align: center; color: Red ;"> Apply Leave </a> ')
            else:
                return HttpResponse('<h2> Invalid Date </h2> <br>  <a href = \'\' '
                                    'style = "text-align: center; color: Red ;"> Apply Leave </a> ')
        elif not request.user.student.room_allotted:
            return HttpResponse('<h3>First Select a Room </h3> <br> <a href = \'select\''
                                ' style = "text-align: center; color: Red ;"> SELECT ROOM </a> ')
        else:
            form = LeaveForm()
            return render(request, 'leave_form.html', {'form': form})
    else:
        form = LeaveForm()
    return render(request,'leave.html',{'form':form})


def maintainence(request):
    pass

def Warden_add_room(request):
    pass




