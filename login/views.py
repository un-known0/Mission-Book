from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from member.models import Member, Title, Graduation
from member.forms import MemberCreationForm, LoginForm, ChangeProfileForm, ChangeNameForm
from django.views.generic import View
from django.http import HttpResponse
import pdb
from PIL import Image
import os, io
import datetime


this_year = 2023


def join(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('success')
    else:
        form = MemberCreationForm()
    return render(request, 'join.html', {'form': form })

def success(request):#테스트용
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.user_id  # 혹은 request.user.username 등 로그인한 유저의 정보를 사용

    context = {
        'user_id': user_id
    }
    return render(request, 'success.html', {"context":context})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            user = authenticate(request, user_id=user_id, password=password)
            # pdb.set_trace()
            if user is not None:
                login(request, user)
                return redirect('success')
            else:
                form.add_error('user_id', '로그인 정보가 잘못되었습니다.')
        return render(request, 'login.html', {'form': form})
    

def logout_member(request):
    logout(request)
    return redirect('/login/')


def is_login(request):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.user_id  # 혹은 request.user.username 등 로그인한 유저의 정보를 사용

    if not user_id:
        return redirect('success')
    
    if datetime.datetime.now().year!=this_year:
        return frashman_graduation(request)

    return 0
    

def profile(request):
    login = is_login(request)
    if login != 0:
        return login
    
    return render(request, 'profile.html')

    
def change_profile(request):
    login = is_login(request)
    if login != 0:
        return login

    user_id = request.user.user_id
    
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_image = form.cleaned_data['profile_image']
            member = Member.objects.get(user_id=user_id)
            img = Image.open(profile_image)
            img = img.convert('RGB')  # RGBA -> RGB 변환
            img = img.resize((100, 100))
            buffer = io.BytesIO()
            img.save(buffer, "JPEG")
            member.profile_image.save(profile_image.name, buffer, save=True)
            return redirect('profile')
    else:
        form = ChangeProfileForm()
    return render(request, 'change_profile.html', {'form': form })



def change_name(request):
    login = is_login(request)
    if login != 0:
        return login

    if request.method == 'POST':
        form = ChangeNameForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['name']
            member = Member.objects.get(user_id=user_id)
            member.name = new_name
            member.save()
            return redirect('profile')
    else: 
        form = ChangeNameForm()
    return render(request, 'change_name.html', {'form': form })



def select_title(request):
    login = is_login(request)
    if login != 0:
        return login
    
    titles = Title.objects.all()

    # Divide titles into selectable and non-selectable
    selectable_titles = []
    non_selectable_titles = []
    for title in titles:
        if request.user.can_select_title(title):
            selectable_titles.append(title)
        else:
            non_selectable_titles.append(title)

    context = {
        'selectable_titles': selectable_titles,
        'non_selectable_titles': non_selectable_titles,
    }
    return render(request, 'select_title.html', context)


def change_title(request, title):
    login = is_login(request)
    if login != 0:
        return login
    
    user_id = request.user.user_id
    
    title = Title.objects.get(id=title)
    if request.user.can_select_title(title):
        member = Member.objects.get(user_id=user_id)
        member.title = title
        member.save()
    return redirect(select_title)


def change_title_color(request, color):
    login = is_login(request)
    if login != 0:
        return login

    user_id = request.user.user_id
    
    if 0<=color<6:
        member = Member.objects.get(user_id=user_id)
        member.title_color = color
        member.save()
    return redirect(select_title)


def frashman_graduation(request):    
    graduation = Graduation.objects.all().order_by('-order')
    for g in graduation:
        if request.user.can_graduation(g):
            return render(request,"frashman_graduation.html",{"graduation":g})
    
