from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import SignupForm, UserProfileForm, UserLoginForm, PasswordResetForm, PasswordChangeCustomForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,force_text
from django.urls import reverse
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
import requests

# Create your views here.

def send_activation_email(aal_user,request):
    email_subject = '30 PiXEl | Activate Your Account'
    email_body = render_to_string('signup/account-activation/account_activation_email.html',{
        'user' : aal_user,
        'site_domain' : get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(aal_user.pk)),
        'token' : generate_token.make_token(aal_user)
    })
    email = EmailMessage(from_email=settings.DEFAULT_FROM_EMAIL, to=[aal_user.email],
                        subject=email_subject, body=email_body)
    email.send()

def email_smtp_verification(email_address):
    request_url = 'https://emailverification.whoisxmlapi.com/api/v1?apiKey={}&emailAddress={}'.format(settings.EMAIL_VERIFICATION_WHOISXML_API_KEY,email_address)
    response = requests.get(request_url)
    data_in_dict = response.json()
    if data_in_dict['smtpCheck'] == 'true' and data_in_dict['catchAllCheck'] == 'true':
        return True
    return False

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('shortner'))
        
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            if User.objects.filter(email = form.cleaned_data.get('email')).exists() == False:
                if email_smtp_verification(form.cleaned_data.get('email')):
                    form.save()
                    username = form.cleaned_data.get('username')
                    aal_user = User.objects.get(username = username)
                    aal_user.username = aal_user.username.lower()
                    aal_user.save()
                    profile_model = UserProfile(username = User.objects.get(username = aal_user.username),email_verified = 'False')
                    profile_model.save()
                    send_activation_email(aal_user,request)
                    return render(request,"signup/signup_success.html",{
                        'username' : username
                    })
                messages.info(request,"Provided Email Address is invalid as SMTP connection breaks.")
                return HttpResponseRedirect(reverse('signup-page'))
            else:
                messages.info(request,'Email Address Already Exist')
                return HttpResponseRedirect(reverse('signup-page'))
            
    else:
        form = SignupForm()
    return render(request,"signup/signup.html" ,{
        'form' : form
    })

@login_required()
def userprofile(request):
    if request.method == "POST":
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            login_user=request.user.username
            user = User.objects.get(username = login_user)
            if authenticate(username = user, password = form.cleaned_data.get('password')):
                user.first_name = form.cleaned_data.get('first_name').capitalize()
                user.last_name = form.cleaned_data.get('last_name').capitalize()
                if user.first_name.isalpha() and user.last_name.isalpha():
                    if user.email == form.cleaned_data.get('email'):
                        user.save()
                        return HttpResponseRedirect(reverse('shortner'))
                    else:
                        if User.objects.filter(email = form.cleaned_data.get('email')).exists() == False:
                            if email_smtp_verification(form.cleaned_data.get('email')):
                                user.email = form.cleaned_data.get('email')
                                user.save()
                                profile_model = UserProfile.objects.get(username__username = user.username)
                                profile_model.email_verified = False
                                profile_model.save()
                                send_activation_email(user,request)
                                messages.info(request,'Verification Link Sent')
                                return HttpResponseRedirect(reverse('logout-action'))
                            messages.info(request,"Provided Email Address is invalid as SMTP connection breaks.")
                            return HttpResponseRedirect(reverse('user-profile-update'))        
                        messages.info(request,'Email Address Already Exist')
                        return HttpResponseRedirect(reverse('user-profile-update'))
                messages.info(request,'Provided Name not Valid')
            else:
                messages.info(request,'Password is not Valid')
            
        return HttpResponseRedirect(reverse('user-profile-update'))
            
    else:
        form = UserProfileForm()
    return render(request,"signup/user-profile-update.html" ,{
        'form' : form
    })

def userlogin(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            if User.objects.filter(username = form.cleaned_data.get('username')).exists():
                valid_user = authenticate(username = form.cleaned_data.get('username'), password = form.cleaned_data.get('password'))
                if valid_user:
                    user_profile_data = UserProfile.objects.get(username__username = form.cleaned_data.get('username'))
                    if user_profile_data.email_verified:
                        login(request,valid_user)
                        if 'next' in request.POST:
                            return redirect(request.POST.get('next')) #request.POST.get(n) --> 'n' is the name of the input data
                        response =  HttpResponseRedirect(reverse('shortner'))
                        response.set_cookie('logined_user',request.user.username,max_age=365*24*60*60)
                        return response
                    messages.info(request, 'Account not activated yet.')
                else:
                    messages.info(request, 'Wrong Password Entered.')
            else:
                messages.info(request, 'Invalid Username given.')
        return HttpResponseRedirect(reverse('user-login-page'))
    
    form = UserLoginForm(initial={'username': request.COOKIES.get('logined_user')})
    return render(request,"signup/login.html",{
        'form' : form
    })
    
def PasswordReset(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            if User.objects.filter(email = form.cleaned_data.get('email')).exists():
                form.save(from_email=settings.DEFAULT_FROM_EMAIL, request=request)
                return HttpResponseRedirect(reverse('password_reset_done'))
            else:
                messages.info(request,"Email Address doesn't exists!")
                return HttpResponseRedirect(reverse('reset_password'))
                
    form = PasswordResetForm()
    return render(request,"signup/password-recovery/password_reset.html",{
        'form' : form
    })
            

@login_required()    
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password Updation Successful!')
            return HttpResponseRedirect(reverse('shortner'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'signup/change_password.html', {
        'form': form
    })

def activate_user(request,uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None
    
    if user is not None and generate_token.check_token(user,token):
        profile_model = UserProfile.objects.get(username__username = user.username)
        profile_model.email_verified = True
        profile_model.save()
        messages.success(request, 'Account Activation Done.')
        return HttpResponseRedirect(reverse('user-login-page'))
    
    else:
        return render(request, 'signup/account-activation/account_activation_failed.html')