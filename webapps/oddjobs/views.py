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
def home(request):
    context = {}
    # original page
    context['home_user'] = User.objects.get(id = request.user.id)
    return render(request, 'login_home.html', context)

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


def home_login(request):
    return render(request, 'login_home.html')


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


