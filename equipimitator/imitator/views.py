from django.shortcuts import render,redirect
from imitator.models import *
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import serializers
from datetime import datetime
from datetime import timedelta
import time
import os,base64
import json
# Create your views here.

@csrf_exempt
def index(request):
    type = request.GET.get('type','全部')
    search = request.GET.get('search','')
    if(type!='全部'):
        e_list = EquipmentTotal.objects.filter(e_type = type,e_name__contains = search).all()
    else:
        e_list = EquipmentTotal.objects.filter(e_name__contains = search).all()
    if(search!=''):
        type = '搜索结果'
    ta_list = EquipmentTAttri.objects.all()
    tsk_list = EquipmentTSk.objects.all()
    sy_list = EquipmentSynthesis.objects.all()
    search += ' '
    context = {'type':type, 'e_list':e_list, 'ta_list':ta_list, 'tsk_list':tsk_list, 'sy_list':sy_list, 'search':search}
    return render(request,'index.html',context = context)

@csrf_exempt
def register(request):
    return render(request,'register.html')

@csrf_exempt
def register_get(request):
    msg = ''
    email = request.GET.get('email','')
    username = request.GET.get('username','')
    password = request.GET.get('password','')
    again = request.GET.get('again','')
    if email == '' or username == '' or password == '' or again == '':
        msg='请完善注册信息！'
        return render(request,'register.html',{'msg':msg})
    if User.objects.filter(email = email):
        msg = '账号已存在！'
        return render(request,'register.html',{'msg':msg})
    
    if User.objects.filter(username = username):
        msg = '昵称已被使用！'
        return render(request,'register.html',{'msg':msg})
    if password != again:
        msg = '密码不一致！'
        return render(request,'register.html',{'msg':msg})
    print(again)
    user = User.objects.create_user(email=email,username=username,password=password)
    user.save()
    msg = '注册成功，请登录！'
    return render(request,'login.html',{'msg':msg})

@csrf_exempt
def login(request):
    return render(request,'login.html')
    
@csrf_exempt
def login_post(request):
    msg = ''
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request,username=username,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            request.session['user'] = username
            return redirect('/index/?type=%s'%'全部')
        else:
            msg = "账号或密码错误！"
    return render(request,'login.html',{'msg':msg})

@csrf_exempt
def equipitem(request):
    id = request.GET.get("e_no")
    item = EquipmentTotal.objects.filter(e_no = id).first()
    ta_list = EquipmentTAttri.objects.all()
    tsk_list = EquipmentTSk.objects.all()
    sy_list = EquipmentSynthesis.objects.all()
    context = {'item':item, 'ta_list':ta_list, 'tsk_list':tsk_list, 'sy_list':sy_list}
    return render(request,'equipitem.html',context = context)
    

@login_required
@csrf_exempt
def login_out(request):
    auth.logout(request)
    return redirect('index')

@login_required
@csrf_exempt
def yourImitator(request):
    e_list = EquipmentTotal.objects.all()
    ta_list = EquipmentTAttri.objects.all()
    tsk_list = EquipmentTSk.objects.all()
    sy_list = EquipmentSynthesis.objects.all()
    context = {'e_list':e_list, 'ta_list':ta_list, 'tsk_list':tsk_list, 'sy_list':sy_list}
    return render(request,'yourImitator.html', context = context)

@login_required
@csrf_exempt
def equipsave(request):
    no1 = request.POST.get("no1")
    no2 = request.POST.get("no2")
    no3 = request.POST.get("no3")
    no4 = request.POST.get("no4")
    no5 = request.POST.get("no5")
    no6 = request.POST.get("no6")
    e_list = []
    if no1:
        e_list.append(EquipmentTotal.objects.filter(e_no = no1).first())
    if no2:
        e_list.append(EquipmentTotal.objects.filter(e_no = no2).first())
    if no3:
        e_list.append(EquipmentTotal.objects.filter(e_no = no3).first())
    if no4:
        e_list.append(EquipmentTotal.objects.filter(e_no = no4).first())
    if no5:
        e_list.append(EquipmentTotal.objects.filter(e_no = no5).first())
    if no6:
        e_list.append(EquipmentTotal.objects.filter(e_no = no6).first())
    p_total = 0
    tp_total = 0
    for i in e_list:
        p_total += i.e_price
        tp_total += i.e_tprice
    
    
    ta_list = []
    for i in e_list:
        for j in EquipmentTAttri.objects.filter(e_no = i).all():
            ta_list.append(j)
    asum_list = []
    for i in EquipmentAttribute.objects.all():
        data = i.e_aname + " + "
        sum = 0
        for j in ta_list:
            if j.e_ano == i and j.e_adata.isdigit():
                sum += int(j.e_adata)
            elif j.e_ano == i:
                sum += float(j.e_adata.strip('%'))/100
        if i.e_aname == '攻击速度' and sum > 2:
            sum = 2.0
        if i.e_aname == '暴击几率' and sum > 1:
            sum = 1.0
        if i.e_aname == '物理吸血' and sum > 1:
            sum = 1.0
        s = str(sum)
        if s.count('.') > 0:
            s = str(float('%.2f'%(sum*100))) + "%"
        data += str(s)
        if sum != 0:
            asum_list.append(data)
        print(data)
    sk_list = []
    for i in e_list:
        for j in EquipmentTSk.objects.filter(e_no = i).all():
            has_exist = 0
            for k in sk_list:
                if j.sk_no.sk_no == k.sk_no.sk_no:
                    has_exist = 1
            if has_exist == 0:
                sk_list.append(j)
    print(sk_list)
    context = {'e_list':e_list, 'p_total':p_total, 'tp_total':tp_total, 'asum_list':asum_list, 'sk_list':sk_list}
    return render(request,'equipsave.html', context = context)

@login_required
@csrf_exempt
def equipsaveover(request):
    name = request.POST.get('name','默认')
    print(name)
    items = request.POST.get('items')
    item = items.split(',')
    print(item)
    if len(item) > 0 and item[0]:
        item1 = EquipmentTotal.objects.filter(e_no = item[0]).first()
    else:
        item1 = EquipmentTotal.objects.filter(e_no = 96).first()
    if len(item) > 1 and item[1]:   
        item2 = EquipmentTotal.objects.filter(e_no = item[1]).first()
    else:
        item2 = EquipmentTotal.objects.filter(e_no = 96).first()
    if len(item)> 2 and item[2]:
        item3 = EquipmentTotal.objects.filter(e_no = item[2]).first()
    else:
        item3 = EquipmentTotal.objects.filter(e_no = 96).first()
    if len(item) > 3 and item[3]:
        item4 = EquipmentTotal.objects.filter(e_no = item[3]).first()
    else:
        item4 = EquipmentTotal.objects.filter(e_no = 96).first()
    if len(item) > 4 and item[4]:
        item5 = EquipmentTotal.objects.filter(e_no = item[4]).first()
    else:
        item5 = EquipmentTotal.objects.filter(e_no = 96).first()
    if len(item) > 5 and item[5]:
        item6 = EquipmentTotal.objects.filter(e_no = item[5]).first()
    else:
        item6 = EquipmentTotal.objects.filter(e_no = 96).first()
    cs = EquipmentSet.objects.create(s_name = name, s_owner = request.user, s_item1 = item1, s_item2 = item2, s_item3 = item3, s_item4 = item4, s_item5 = item5, s_item6 = item6)
    cs.save()
    return redirect('yourIndex')

@login_required
@csrf_exempt
def yourIndex(request):
    user = request.user
    s_list = EquipmentSet.objects.filter(s_owner = user)
    context = {'s_list':s_list}
    return render(request,'yourIndex.html', context = context)
    
@login_required
@csrf_exempt    
def equipset(request):
    id = request.GET.get('s_no')
    set = EquipmentSet.objects.filter(s_no = id).first()
    e_list = []
    if set.s_item1 and set.s_item1.e_no != 96:
        e_list.append(set.s_item1)
    if set.s_item2 and set.s_item2.e_no != 96:
        e_list.append(set.s_item2)
    if set.s_item3 and set.s_item3.e_no != 96:
        e_list.append(set.s_item3)
    if set.s_item4 and set.s_item4.e_no != 96:
        e_list.append(set.s_item4)
    if set.s_item5 and set.s_item5.e_no != 96:
        e_list.append(set.s_item5)
    if set.s_item6 and set.s_item6.e_no != 96:
        e_list.append(set.s_item6)
    p_total = 0
    tp_total = 0
    for i in e_list:
        p_total += i.e_price
        tp_total += i.e_tprice
    
    
    ta_list = []
    for i in e_list:
        for j in EquipmentTAttri.objects.filter(e_no = i).all():
            ta_list.append(j)
    asum_list = []
    for i in EquipmentAttribute.objects.all():
        data = i.e_aname + " + "
        sum = 0
        for j in ta_list:
            if j.e_ano == i and j.e_adata.isdigit():
                sum += int(j.e_adata)
            elif j.e_ano == i:
                sum += float(j.e_adata.strip('%'))/100
        if i.e_aname == '攻击速度' and sum > 2:
            sum = 2.0
        if i.e_aname == '暴击几率' and sum > 1:
            sum = 1.0
        if i.e_aname == '物理吸血' and sum > 1:
            sum = 1.0
        s = str(sum)
        if s.count('.') > 0:
            s = str(float('%.2f'%(sum*100))) + "%"
        data += str(s)
        if sum != 0:
            asum_list.append(data)
        print(data)
    sk_list = []
    for i in e_list:
        for j in EquipmentTSk.objects.filter(e_no = i).all():
            has_exist = 0
            for k in sk_list:
                if j.sk_no.sk_no == k.sk_no.sk_no:
                    has_exist = 1
            if has_exist == 0:
                sk_list.append(j)
    print(sk_list)
    context = {'set':set, 'e_list':e_list, 'p_total':p_total, 'tp_total':tp_total, 'asum_list':asum_list, 'sk_list':sk_list}
    return render(request,'equipset.html', context = context)

@login_required
@csrf_exempt    
def equipdelete(request):
    set_no = request.POST.get("set_no")
    print(set_no)
    set = EquipmentSet.objects.filter(s_no = set_no).delete()
    return redirect(yourIndex)
    
@csrf_exempt    
def aboutAuthor(request):
    return render(request,'aboutAuthor.html')

@login_required
@csrf_exempt    
def setcolor(request):
    s_no = request.POST.get('s_no')
    color = request.POST.get('s_color')
    set = EquipmentSet.objects.filter(s_no = s_no).first()
    set.s_color = color
    set.save()
    return redirect('yourIndex')