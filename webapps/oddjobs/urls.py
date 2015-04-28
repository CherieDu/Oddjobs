from django.conf.urls import patterns, include, url
from django.contrib import admin
from forms import *

urlpatterns = patterns('',
    url(r'^$', 'oddjobs.views.home', name='home'),
    # url(r'^home', 'oddjobs.views.home', name='home'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'non_login_home.html','authentication_form': LoginForm,'extra_context':{'Registerform':RegistrationForm}}, name = 'login'),
    #url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'non_login_home.html'},name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^register$', 'oddjobs.views.register',name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'oddjobs.views.confirm_registration', name='confirm'),
    url(r'^forgotPassword', 'oddjobs.views.forgotPassword',name='forgotPassword'),
    url(r'^reset_forgot_password/(?P<email>[a-zA-Z0-9_@\+\-.]+)/(?P<token>[a-z0-9\-]+)$', 'oddjobs.views.reset_forgot_password',name='resetForgotPassword'),
    url(r'^getProfilePhoto/(?P<id>\d+)$', 'oddjobs.views.getProfilePhoto', name='getProfilePhoto'),
    url(r'^addJob$', 'oddjobs.views.addJob',name='addJob'),

)