from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from .forms import UserRegistrationform, StoryAddForm,AddBlog
from django.forms import ValidationError, forms
from django.contrib.auth.models import User
from .models import Story,Blog


# Create your views here.

def home(request):
    return render(request, 'sayonestories/home.html', context={})


def userregisterform(request):
    form = UserRegistrationform()
    return render(request, 'sayonestories/userregistration.html', context={'form': form})


def validate_register(request):
    if request.method == 'POST':
        form = UserRegistrationform(request.POST, request.FILES)
        if form.is_valid():
            sayone = form.save(commit=False)
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['mailid']
            password = userObj['password']
            cnf_password = userObj['cnf_pass']

            error_codes = []
            if User.objects.filter(email=email).exists():
                error_codes.append('email_exists')
            elif User.objects.filter(username=username).exists():
                error_codes.append('username_exists')
            elif password != cnf_password:
                error_codes.append('passwords_nomatch')

            print("///", error_codes)

            if 'email_exists' in error_codes:
                form.errors['mailid'] = form.error_class(['Mail ID already in use'])

            elif 'username_exists' in error_codes:
                form.errors['username'] = form.error_class(['username already taken'])
            elif 'passwords_nomatch' in error_codes:
                form.errors['password'] = form.error_class(['passwords did not match'])

            if len(error_codes) == 0:
                sayoneuser = User.objects.create_user(username=username, email=email, password=password)
                sayone.user = sayoneuser
                sayone.save()
                return redirect('home')
            else:
                return render(request, 'sayonestories/userregistration.html', context={'form': form})



    else:
        form = UserRegistrationform()

    return render(request, 'sayonestories/userregistration.html', {'form': form})


def User_profile_page(request):
    pic_url = request.user.sayone_user.profile_pic
    data = Blog.objects.all()
    print('blogs....',data)
    return render(request, 'sayonestories/UserHome.html', context={'img_url': pic_url})


def add_story_page(request):
    form = StoryAddForm()
    return render(request, 'sayonestories/addstory.html', context={'form': form})


def add_story(request):
    if request.method == 'POST':
        form = StoryAddForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            print('/////',request.user)
            profile.story_user = request.user

            profile.save()
            return redirect('add_sub_story')
        else:
            return render(request, 'sayonestories/addstory.html', context={'form': form})
    else:
        form = StoryAddForm()
        render(request, 'sayonestories/addstory.html', context={'form': form})


def add_sub_story(request):

    story_object = Story.objects.latest('story_id')
    if story_object.story_type in [0,1]:

        return render(request,'sayonestories/addstory.html',context={'story':story_object,'form1':form1})
    else:
        return render(request,'sayonestories/addstory.html',context={'story':story_object})


def add_blog(request):
    print('call here')
    story_id = request.POST.get('storyid')
    story_obj = Story.objects.filter(story_id=story_id)
    print('ssss',story_obj)

    if request.method == 'POST':
        form = AddBlog(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.story = story_obj[0]
            blog.save()
            return render(request, 'sayonestories/Loginpage.html',context={})
        else:
            return render(request,'sayonestories/addstory.html',context={})
    else:
        return render(request,'sayonestories/addstory.html',context={})



