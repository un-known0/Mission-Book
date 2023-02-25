from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from member.models import Member, Title, Graduation
from checklist.models import Checklist,MemberChecklist
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
            checklists = Checklist.objects.all()
            for c in range(len(checklists)):
                print("hi")
                MemberChecklist.objects.create(member=request.user.user_id, checklist=checklists[c], status=-1)        
            return redirect('/prolog/1')
    else:
        form = MemberCreationForm()
    return render(request, 'join.html', {'form': form })


def index_null(request):
    return index(request,1)


def index(request, category):

    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.user_id  # 혹은 request.user.username 등 로그인한 유저의 정보를 사용
    
    if user_id and datetime.datetime.now().year!=this_year:
        return redirect('/ending/1')
    
    checklists = MemberChecklist.objects.filter(member=user_id)
    if category == 1:
        some_missionlist_pro = checklists.filter(checklist__category=1, status=0, checklist__need_class_stat__lte=request.user.int_stat)  # 카테고리가 1, status가 0인 미션 리스트를 가져옴
        some_missionlist_pre = checklists.filter(checklist__category=1, status=-1, checklist__need_class_stat__lte=request.user.int_stat) # 카테고리가 1, status가 -1인 미션 리스트를 가져옴
        some_missionlist_pro.order_by('checklist__level')
        some_missionlist_pre.order_by('checklist__level')
        category_name = '학업'
    elif category == 2:
        some_missionlist_pro = checklists.filter(checklist__category=2, status=0, checklist__need_social_stat__lte=request.user.social_stat)  # 카테고리가 2, status가 0인 미션 리스트를 가져옴
        some_missionlist_pre = checklists.filter(checklist__category=2, status=-1, checklist__need_social_stat__lte=request.user.social_stat)  # 카테고리가 2, status가 -1인 미션 리스트를 가져옴
        some_missionlist_pro.order_by('checklist__level')
        some_missionlist_pre.order_by('checklist__level')
        category_name = '사교'
    elif category == 3:
        some_missionlist_pro = checklists.filter(checklist__category=3, status=0, checklist__need_exp_stat__lte=request.user.exp_stat)  # 카테고리가 3, status가 0인 미션 리스트를 가져옴
        some_missionlist_pre = checklists.filter(checklist__category=3, status=-1, checklist__need_exp_stat__lte=request.user.exp_stat)  # 카테고리가 3, status가 -1인 미션 리스트를 가져옴
        some_missionlist_pro.order_by('checklist__level')
        some_missionlist_pre.order_by('checklist__level')
        category_name = '경험'
    else:
        some_missionlist = None
    context = {'some_missionlist_pre': some_missionlist_pre,
               'some_missionlist_pro':some_missionlist_pro,'category_name':category_name}
    return render(request, 'index.html', context)    
    

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
            if user is not None:
                login(request, user)
                return redirect('index_null')
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
        return redirect('index_null')
    
    if datetime.datetime.now().year!=this_year:
        return redirect('/ending/1')

    return 0
    

def profile(request):
    login = is_login(request)
    if login != 0:
        return login
    
    return render(request, 'profile.html')

def mypage(request):
    login = is_login(request)
    if login != 0:
        return login
    
    titles = Title.objects.all()

    selectable_titles = []
    for title in titles:
        if request.user.can_select_title(title):
            selectable_titles.append(title)
            
    int_num = 0
    social_num = 0
    exp_num = 0
    
    checklists = MemberChecklist.objects.filter(member=request.user.user_id, status = 1)
    for check in checklists:
        if check.checklist.category == 1:
            int_num+=1
        elif check.checklist.category == 2:
            social_num+=1
        else: 
            exp_num+=1


    context = {
        'selectable_titles': selectable_titles,
        'exp_per':str(int((request.user.total_exp%1)*100)),
        'int_num' : int_num,
        'social_num' : social_num,
        'exp_num' : exp_num,
        'total_num' : int_num+social_num+exp_num
    }
    return render(request, 'mypage.html', context)

    
def setup(request):
    login = is_login(request)
    if login != 0:
        return login
    user_id = request.user.user_id
    
    if request.method == 'POST':
        if 'change_profile' in request.POST:
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
                return redirect('mypage')
        elif 'change_name' in request.POST:
            form = ChangeNameForm(request.POST)
            if form.is_valid():
                new_name = form.cleaned_data['name']
                member = Member.objects.get(user_id=user_id)
                if new_name != member.name: # 변경된 이름이 있는 경우에만 업데이트
                    member.name = new_name
                    member.save()
                return redirect('mypage')
        elif 'unregister' in request.POST:
            user_id = request.user.user_id
            member = Member.objects.get(user_id=user_id)
            member.is_active = False
            member.save()
            return redirect('index_null')

    form1 = ChangeProfileForm()
    form2 = ChangeNameForm()
    return render(request, 'setup.html', {'form1': form1, 'form2': form2 })



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
    return redirect('mypage')


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


def ending(request, num):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.user_id

    if not user_id and datetime.datetime.now().year==this_year:
        return redirect('index_null')

    if num == 1:
        return render(request, "ending.html")
    elif num == 2:
        return render(request, "ending2.html")
    elif num == 3:
        int_num = 0
        social_num = 0
        exp_num = 0
        
        checklists = MemberChecklist.objects.filter(member=request.user.user_id, status = 1)
        for check in checklists:
            if check.checklist.category == 1:
                int_num+=1
            elif check.checklist.category == 2:
                social_num+=1
            else: 
                exp_num+=1
        total_num = int_num+social_num+exp_num
        graduation = Graduation.objects.all().order_by('-order')
        for g in graduation:
            if request.user.can_graduation(g):
                return render(request, "ending3.html", {"graduation": g, "int_num":int_num,"social_num":social_num,"exp_num":exp_num,"total_num":total_num})
        


def prolog(request, num):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.user_id

    if not user_id and datetime.datetime.now().year!=this_year:
        return redirect('index_null')

    if num == 1:
        return render(request, "prolog.html")
    elif num == 2:
        return render(request, "prolog2.html")



