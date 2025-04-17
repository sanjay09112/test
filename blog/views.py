from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
import logging
from . models import Category, Post,Aboutus
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

from .forms import ContactForm, ForgetPasswordForm , LoginForm, PostForm,RegisterForm, ResetPasswordForm

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.

#static data
# posts=[
#         {'id':'1','title':'post 1','content':'content of post 1'},
#         {'id':'2','title':'post 2','content':'content of post 2'},
#         {'id':'3','title':'post 3','content':'content of post 3'},
#         {'id':'4','title':'post 4','content':'content of post 4'}
#     ]

def index(request):
    blog_title="Latest Posts"
    posts=Post.objects.all()
    return render(request,'index.html',{"blog_title":blog_title,'posts':posts})

def detail(request,post_id):
    # static data
    # post=next((item for item in posts if item['id']==int(post_id)),None)
    try:
        post=Post.objects.get(pk=post_id)
        related_posts=Post.objects.filter(category=post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404('page does not exist') 
    # logger =logging.getLogger("Testing")
    # logger.debug(f'post variable is {post}')
    return render(request,'detail.html',{'post':post,'related_posts':related_posts})

def display2(request):
    return HttpResponse("you are at detail page")

def id(request,post_id):
    return HttpResponse(f"Your post id is:{post_id}")

def old_url_redirect(request):
    return redirect(reverse("blog:new"))

def new_url_view(request):
    return HttpResponse("You are at new url...")

def contact_view(request):
    if(request.method)=="POST":
        form=ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        logger =logging.getLogger("Testing")
        if form.is_valid():
            logger.debug(f'post Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            success_message = 'Your Email has been sent!'
            return render(request,'contact.html', {'form':form,'success_message':success_message})
        else:
            logger.debug("Form validation failure")
        return render(request,'contact.html',{'form':form})
    return render(request,'contact.html')


def about_view(request):
    about_content = Aboutus.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default content goes here."  # Replace with your desired default string
    else:
        about_content = about_content.content
    return render(request,'about.html',{'about_us':about_content})


def register(request):
    form=RegisterForm()
    if(request.method == 'POST'):
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,"Registration Successfull. You can log in")
            return redirect("blog:login")
    return render(request,'register.html',{'form':form})

def login(request):
    form=LoginForm()
    if(request.method=='POST'):
        form=LoginForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if(user is not None):
                auth_login(request,user)
                return redirect("blog:dashboard")
                print('Login success')
    return render(request,'login.html',{'form':form})

def dashboard(request):
    blog_title='My Posts'
    all_posts=Post.objects.filter(user=request.user)
    return render (request,'dashboard.html',{'blog_title':blog_title,'posts':all_posts})

def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forget_password(request):
    form = ForgetPasswordForm()
    if request.method == 'POST':
        #form
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            #send email to reset password
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "Reset Password Requested"
            message = render_to_string('reset_password_email.html', {
                'domain': domain,
                'uid': uid,
                'token': token
            })

            send_mail(subject, message, 'noreply@jvlcode.com', [email])
            messages.success(request, 'Email has been sent')


    return render(request,'forget_password.html', {'form': form})

def reset_password(request, uidb64, token):
    form = ResetPasswordForm()
    if request.method == 'POST':
        #form
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('blog:login')
            else :
                messages.error(request,'The password reset link is invalid')

    return render(request,'reset_password.html', {'form': form})

def new_post(request):
    categories=Category.objects.all()
    form=PostForm()
    if request.method == 'POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('blog:dashboard')
    return render(request,'new_post.html',{'categories':categories,'form':form})