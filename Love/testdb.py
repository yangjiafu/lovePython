# encoding: utf-8
import json
import random
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from App.models import TbMovies, TbUsers
# from App.models import *
from django.conf import settings
from django.core.mail import send_mail
import settings
import threading
import hashlib
import os

# name = ''
# pwd = ''
# email = ''
# gender = ''
# age = ''
# email_code = ''
# login_classify = ''


def send_email(mail):
    rs = random.sample('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 4)
    rs = ''.join(rs)
    msg = u'你的随机验证码为：<a style="color:red">%s</a>' % rs
    send_mail(u'验证码', 'actions', settings.EMAIL_HOST_USER,
              [mail],
              html_message=msg
              )
    return rs


def detection(account):
    try:
        info = TbUsers.objects.get(u_account=account)
        if info.is_active != '1':
            TbUsers.objects.filter(u_account=account).delete()
        else:
            pass
    except:
        pass


@csrf_exempt
def usersdb(request):
    # list = TbUsers.objects.all()
    # for i in list:
    #     print i.u_name,i.u_id,i.u_email
    # return HttpResponse('查询成功')
    if request.GET:
        a = request.GET['a']
        b = request.GET['b']
        a = int(a)
        b = int(b)
        return HttpResponse(str(a+b))
    elif request.POST:
        a = request.POST['a']
        b = request.POST['b']
        a = int(a)
        b = int(b)
        l = '%s%s' % ('这个数和是：',a+b)
        return HttpResponse(l)


@csrf_exempt
def userlogin(request):
    if request.POST:
        try:
            res = TbUsers.objects.get(u_account=request.POST['account'])
            if request.POST['pwd'] == res.u_pwd:
                tokens = hashlib.sha1(os.urandom(24)).hexdigest()
                TbUsers.objects.filter(u_id=res.u_id).update(token=tokens, u_ip=request.POST['ip'])
                s = {'id': res.u_id, 'pwd': res.u_pwd, 'name': res.u_name, 'email': res.u_email, 'vip': res.u_vip, 'token': tokens}
                return HttpResponse(json.dumps(s), content_type='application/json')
            else:
                return HttpResponse(u'密码错误')
        except:
            return HttpResponse(u'未找到该用户')


@csrf_exempt
def tokenLogin(request):
    if request.POST:
        try:
            res = TbUsers.objects.get(token=request.POST['token'])
            print request.POST['ip']
            if res.u_ip == request.POST['ip']:
                s = {'id': res.u_id, 'pwd': res.u_pwd, 'name': res.u_name, 'email': res.u_email, 'vip': res.u_vip, 'token': res.token}
                return HttpResponse(json.dumps(s), content_type='application/json')
            else:
                return HttpResponse(u'禁止异地token登录')
        except:
            return HttpResponse(u'loginErr')


@csrf_exempt
def getEmailCode(request):
    if request.POST:
        try:
            TbUsers.objects.get(u_account=request.POST['account'])
            return HttpResponse(u'账号已被注册')
        except:
            try:
                TbUsers.objects.get(u_email=request.POST['email'])
                return HttpResponse(u'邮箱已被注册')
            except:
                account = request.POST['account']
                name = request.POST['name']
                pwd = request.POST['pwd']
                email = request.POST['email']
                gender = request.POST['gender']
                age = request.POST['age']
                code = send_email(email)
                tbuser = TbUsers(u_account=account, u_name=name, u_pwd=pwd, u_age=age, u_email=email, u_gender=gender, u_code=code)
                tbuser.save()
                # 60s后检测是否注册成功，如果未注册则删除此条记录
                change = threading.Timer(61.0, detection, (account,))
                change.start()
                return HttpResponse(u'信息暂时存入数据库')


@csrf_exempt
def registered(request):
    if request.POST:
        try:
            account = request.POST['account']
            info = TbUsers.objects.get(u_account=account)
            u_code = info.u_code
            is_active = info.is_active
            if u_code == request.POST['code'] and is_active != '1':
                TbUsers.objects.filter(u_account=account).update(is_active='1')
                return HttpResponse('issuccess')
            else:
                return HttpResponse('code is err')
        except:
            return HttpResponse(u'账号不存在')


@csrf_exempt
def search(request):
    if request.POST:
        try:
            movie = request.POST['movie']
            # print movie
            if len(movie) > 0:
                movies = TbMovies.objects.filter(m_name__contains=movie)
                info = []
                for i in movies:
                    ins = {'id': i.m_id, 'name': i.m_name, 'othername': i.m_othername, 'cover': i.m_cover, 'actor': i.m_actor, 'director': i.m_director, 'classify': i.m_classify, 'area': i.m_area, 'language': i.m_language,
                           'releasetime': i.m_releasetime, 'duration': i.m_duration, 'score': i.m_score, 'synopsis': i.m_synopsis, 'linkInfo': i.m_linkinfo}
                    info.append(ins)
                return HttpResponse(json.dumps(info), content_type='application/json')
            else:
                return HttpResponse('err')
        except:
            return HttpResponse('search err')