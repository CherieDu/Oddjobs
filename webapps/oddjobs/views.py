from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.db import transaction
# Create your views here.

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from mimetypes import guess_type


from django.http import HttpResponse, Http404

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from models import *
from forms import *
import json
import datetime
import time
from django.http import JsonResponse
from django.db.models import Q


@login_required
@transaction.atomic
def make_userinfo_view(request, 
                currentUser=[],
                userinfo=[],
                html="",
                user = [],
                userToShow=[],
                jobs=[],
                create_job_form=JobForm(),
                create_userinfo_form=UserInfoForm(), 
                create_register_form=RegistrationForm(),
                create_changePassword_form=ResetPasswordForm()
                ):

    context = {
                'username':currentUser,
                'userinfo':userinfo,
                'jobs':jobs,
                'user' : user,
                'userToShow':userToShow,
                'create_job_form':create_job_form,
                'create_userinfo_form':create_userinfo_form,
                'create_register_form':create_register_form,
                'create_changePassword_form':create_changePassword_form,
              }
    return render(request, html, context)



@login_required
@transaction.atomic
def home(request):
    
    new_job = Job(user=request.user)
    jobform=JobForm(instance=new_job)

    html = 'login_home.html'
    currentUser = request.user
    user = User.objects.get(username=request.user)
    userInfoToEdit = get_object_or_404(UserInfo, user=currentUser)
    userToShow = request.user
    userinfo_form = UserInfoForm(request.POST,request.FILES, instance=userInfoToEdit)
    jobs = Job.objects.filter(user=request.user).order_by('-date_created')
    return make_userinfo_view(request=request, 
        html=html, 
        jobs=jobs,
        user = user,
        create_userinfo_form=userinfo_form,
        userToShow=userToShow,
        create_job_form=jobform,
        userinfo=userInfoToEdit,
        currentUser=currentUser)

@transaction.atomic
def register(request):

    context = {}
    context['form'] = LoginForm()

    if request.method == 'GET':
        context['Registerform'] = RegistrationForm()
        return render(request, 'non_login_home.html', context)
    
    Registerform = RegistrationForm(request.POST)
    context['Registerform'] = Registerform
    if not Registerform.is_valid():
        return render(request,'non_login_home.html', context)
        
    new_user = User.objects.create_user(username=Registerform.cleaned_data['username'],
                                        email=Registerform.cleaned_data['email'],
                                        password=Registerform.cleaned_data['password1'])
    new_user.save()

    user_info = UserInfo(user=new_user)
    user_info.save()

    new_user.is_active = False
    new_user.save()

    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to Letters.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="chunyued@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = Registerform.cleaned_data['email']
    return render(request, 'needs-confirmation.html', context)


def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})


# def home_login(request):
#     return render(request, 'login_home.html')


@transaction.atomic
def forgotPassword(request):
    context = {}
    context['success'] = 0
    if request.method=='GET':
        context['form'] = ForgotPasswordForm()
        return render(request, 'forgotPassword.html', context)
    form = ForgotPasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'forgotPassword.html', context)
    email = form.cleaned_data['email']
    user = User.objects.get(email=email)
    token = default_token_generator.make_token(user)
    print "in forgotPassword "
    email_body = """
Hi, if you forget your password, click the below link to reset your password:

  http://%s%s
""" % (request.get_host(),reverse('resetForgotPassword', args=(email, token)))

    send_mail(subject="Forgot oddjobs password.",
              message= email_body,
              from_email="chunyued@andrew.cmu.edu",
              recipient_list=[email])
    context['success'] = 1
    context['email'] = form.cleaned_data['email']
    context['confirmationUrl'] = """http://%s%s
""" % (request.get_host(),reverse('resetForgotPassword', args=(email, token)))
    return render(request, 'forgotPassword.html', context) 

@transaction.atomic
def reset_forgot_password(request, email, token):
    context = {}
    context['token'] = token
    context['email'] = email
    user = get_object_or_404(User, email=email)
    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404
    # Otherwise token was valid, listen to the GET or POST request
    if request.method=='GET':
        context['form'] = ResetForgotPasswordForm()
        return render(request, 'reset_forgotten_password.html', context)
    #Request method is post. Update password
    form = ResetForgotPasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'reset_forgotten_password.html', context)
    user.set_password(form.cleaned_data['password1'])
    user.save()

    return redirect('login')


@login_required
@transaction.atomic
def getProfilePhoto(request, id):
    user=User.objects.get(id=id)
    userinfo = get_object_or_404(UserInfo, user=user)
    if not userinfo.picture:
        raise Http404

    content_type = guess_type(userinfo.picture.name)
    return HttpResponse(userinfo.picture, content_type=content_type)

@login_required
@transaction.atomic
def addJob(request):
    new_job = Job(user=request.user)
    html = 'login_home.html'
    if request.method=='GET':
        jobform=JobForm(instance=new_job)
        return redirect(html)

    jobform=JobForm(request.POST, request.FILES, instance=new_job)
    
    if not jobform.is_valid():
        return redirect(html)

    jobform.save()
    currentUser = request.user
    user = User.objects.get(username=request.user),

    userInfoToEdit = get_object_or_404(UserInfo, user=currentUser)
    userToShow = request.user
    userinfo_form = UserInfoForm(request.POST,request.FILES, instance=userInfoToEdit)
    jobs = Job.objects.filter(user=request.user).order_by('-date_created')
    return make_userinfo_view(request=request, 
        html=html, 
        jobs=jobs,
        user = user,
        create_userinfo_form=userinfo_form,
        userToShow=userToShow,
        create_job_form=jobform,
        userinfo=userInfoToEdit,
        currentUser=currentUser)


@login_required
@transaction.atomic
def askingHistory(request):
    username = request.user

    jobs = Job.objects.filter(user=username).order_by('-date_created')
    userinfo = UserInfo.objects.get(user=username)
    
    context = {'username': username, 'jobs' : jobs, 'userinfo':userinfo}

    return render(request, 'asking_history.html', context)


@login_required
@transaction.atomic
def showProfile(request, id):
    currentUser = request.user
    userToShow = User.objects.get(id=id)
    userinfo = get_object_or_404(UserInfo,user=userToShow)
    userInfoForm = UserInfoForm(request.POST, request.FILES, instance=userinfo)
    user = User.objects.get(username=request.user)
    html = 'showProfile.html'
    return make_userinfo_view(request=request,
            currentUser=currentUser,
            userinfo=userinfo,
            html=html,
            user = user,
            create_userinfo_form=userInfoForm,
            userToShow=userToShow)




@login_required
@transaction.atomic
def editProfile(request):
    print 'request', request
    print 'request.user', request.user
    user = User.objects.get(username=request.user)

    if request.method == 'GET':
        return showProfile(request, id = user.id)

    currentUser = request.user
    userinfo = get_object_or_404(UserInfo,user=currentUser)
    html = 'showProfile.html'
    userInfoForm = UserInfoForm(request.POST, request.FILES, instance=userinfo)

    if not userInfoForm.is_valid():

        return showProfile(request, id = user.id)
    else:

        userInfoForm.save()
        currentUser = request.user

        userinfo = get_object_or_404(UserInfo,user=currentUser)
        return make_userinfo_view(request=request,
            currentUser=currentUser,
            userinfo=userinfo,
            html=html,
            user = user,
            create_userinfo_form=userInfoForm)


@login_required
@transaction.atomic
def getJobPhoto(request, id):
    user=request.user
    job = get_object_or_404(Job, id=id)
    if not job.picture:
        raise Http404

    content_type = guess_type(job.picture.name)
    return HttpResponse(job.picture, content_type=content_type)


@login_required
@transaction.atomic
def allJobs(request):
    jobs = Job.objects.all().order_by('-date_created')
    userinfo = UserInfo.objects.get(user=request.user)
    username = request.user
    user = User.objects.get(username=request.user)
    html = "discover.html"
    currentUser = request.user
    return make_userinfo_view(request=request,
            currentUser=currentUser,
            userinfo=userinfo,
            jobs = jobs,
            html=html,
            user = user)

@login_required
@transaction.atomic
def search(request):
    searchText = ''
    html = 'search.html'
    if not (not 'searchText' in request.GET or not request.GET['searchText']):
        searchText = request.GET['searchText']

    
    jobs = Job.objects.filter(content__icontains=searchText).order_by('-date_created')
    userInfos = []
    userInfos = UserInfo.objects.filter(
        Q(firstname__icontains=searchText) | Q(lastname__icontains=searchText))
    userInfos = list(userInfos)
    users = User.objects.filter(username__icontains = searchText)
    for user in users:
        userInfos.append(UserInfo.objects.get(user = user))

    username = request.user
    context = { 'username': username, 'jobs' : jobs, 
                'userInfos': userInfos, 'searchText': searchText}

    return render(request, html, context)


