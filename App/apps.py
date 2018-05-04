# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.apps import AppConfig
from App.models import TbMovies, TbUsers, TbVideo, TbReply, TbComment
import json
import random
from django.core.mail import send_mail
from django import forms

import Love.settings
import threading
import hashlib
import os

class AppConfig(AppConfig):
    name = 'App'


class MovieForm(forms.Form):
    movieName = forms.CharField()
    otherName = forms.CharField()
    actors = forms.CharField()
    director = forms.CharField()
    classify = forms.CharField()
    area = forms.CharField()
    language = forms.CharField()
    releasetime = forms.CharField()
    score = forms.CharField()
    m_poster = forms.FileField()
    m_movie = forms.FileField()


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
    except TbUsers.DoesNotExist:
        pass


class User:
    # 所有用户的基类
    def __init__(self, **kw):
        for k, w in kw.iteritems():
            setattr(self, k, w)
    # def __init__(self, id, account, pwd, gender, age, vip, email, likemovies, duration, recording, recommendmovie, code, ip):
    #     self.id = id
    #     self.account = account
    #     self.pwd = pwd
    #     self.gender = gender
    #     self.age = age
    #     self.vip = vip
    #     self.email = email
    #     self.likemovies =likemovies
    #     self.duration = duration
    #     self.recording = recording
    #     self.recommendmovie = recommendmovie
    #     self.code = code
    #     self.ip = ip

    def user_login(self):
        try:
            res = TbUsers.objects.get(u_account=self.account)
            if self.pwd == res.u_pwd:
                tokens = hashlib.sha1(os.urandom(24)).hexdigest()
                # TbUsers.objects.filter(u_id=res.u_id).update(token=tokens, u_ip=request.POST['ip'])
                s = {'id': res.u_id, 'pwd': res.u_pwd, 'name': res.u_name, 'email': res.u_email, 'vip': res.u_vip, 'token': tokens}
                return json.dumps(s)
            else:
                return u'密码错误'
        except TbUsers.DoesNotExist:
            return u'未找到该用户'

    def user_get_code(self):
        try:
            TbUsers.objects.get(u_account=self.account)
            return u'账号已被注册'
        except TbUsers.DoesNotExist:
            try:
                TbUsers.objects.get(u_email=self.email)
                return u'邮箱已被注册'
            except TbUsers.DoesNotExist:
                code = send_email(self.email)
                tbuser = TbUsers(u_account=self.account, u_name=self.name, u_pwd=self.pwd, u_age=self.age, u_email=self.email, u_gender=self.gender, u_code=code)
                tbuser.save()
                # 60s后检测是否注册成功，如果未注册则删除此条记录
                change = threading.Timer(61.0, detection, (self.account,))
                change.start()
                return u'信息暂时存入数据库'

    def user_register(self):
        try:
            info = TbUsers.objects.get(u_account=self.account)
            u_code = info.u_code
            is_active = info.is_active
            if u_code == self.code and is_active != '1':
                TbUsers.objects.filter(u_account=account).update(is_active='1')
                return 'is success'
            else:
                return 'code is err'
        except TbUsers.DoesNotExist:
            return u'账号不存在'

    def user_token_login(self):
        try:
            res = TbUsers.objects.get(token=self.token)
            if res.u_ip == self.ip:
                s = {'id': res.u_id, 'pwd': res.u_pwd, 'name': res.u_name, 'email': res.u_email, 'vip': res.u_vip,
                     'token': res.token}
                return json.dumps(s)
            else:
                return u'禁止异地token登录'
        except TbUsers.DoesNotExist:
            return 'login error'


class Search:
    def __init__(self, **kw):
        for k, w in kw.iteritems():
            setattr(self, k, w)

    def search_movie(self):
        try:
            movie = self.movie
            if len(movie) > 0:
                movies = TbMovies.objects.filter(m_name__contains=movie)
                info = []
                for i in movies:
                    ins = {'id': i.m_id, 'name': i.m_name, 'othername': i.m_othername, 'cover': i.m_cover, 'actor': i.m_actor, 'director': i.m_director, 'classify': i.m_classify, 'area': i.m_area, 'language': i.m_language,
                           'releasetime': i.m_releasetime, 'duration': i.m_duration, 'score': i.m_score, 'synopsis': i.m_synopsis, 'linkInfo': i.m_linkinfo}
                    info.append(ins)
                return json.dumps(info)
            else:
                return 'too short'
        except TbMovies.DoesNotExist:
            return 'search err'


class Movies:
    def __init__(self, **kw):
        for k, w in kw.iteritems():
            setattr(self, k, w)

    def upload_movie(self):
        mf = MovieForm(self.post, self.files)
        if mf.is_valid():
            movieName = mf.cleaned_data['movieName']
            otherName = mf.cleaned_data['otherName']
            actors = mf.cleaned_data['actors']
            director = mf.cleaned_data['director']
            classify = mf.cleaned_data['classify']
            area = mf.cleaned_data['area']
            language = mf.cleaned_data['language']
            releasetime = mf.cleaned_data['releasetime']
            score = mf.cleaned_data['score']
            m_poster = mf.cleaned_data['m_poster']
            m_movie = mf.cleaned_data['m_movie']
            print movieName
            upData = TbMovies(m_name=movieName, m_othername=otherName, m_actor=actors, m_director=director,
                              m_classify=classify, m_area=area, m_language=language, m_releasetime=releasetime,
                              m_score=score, m_cover=m_poster, m_linkinfo=m_movie)
            upData.save()
            return 'upload success!!'
        else:
            return 'the data have wrong'


class Comment:
    def __init__(self, **kw):
        for k, w in kw.iteritems():
            setattr(self, k, w)

    def get_comment(self):
        id = self.id
        if len(id) > 0:
            comment = TbComment.objects.filter(topic_id=id)
            contens = []
            for c in comment:
                user = TbUsers.objects.get(u_id=c.form_uid)
                form_c_avatar = user.u_avatar if user.u_avatar else ''
                reply = TbReply.objects.filter(reply_id=c.c_id)
                replys = []
                for r in reply:
                    r_user = TbUsers.objects.get(u_id=r.form_uid)
                    form_r_avatar = user.u_avatar if r_user.u_avatar else ''
                    content = {'r_id': r.r_id, 'reply_id': r.reply_id, 'r_content': r.content, 'r_name': r_user.u_name,
                               'r_avatar': form_r_avatar}
                    replys.append(content)
                cins = {'c_id': c.c_id, 'content': c.content, 'topic_id': c.topic_id, 'form_uid': c.form_uid,
                        'form_name': user.u_name, 'form_avatar': form_c_avatar, 'reply': replys}
                contens.append(cins)
            return json.dumps(contens)
            # comments = []
            # replys = []
            # for c in comment:
            #     form_user = TbUsers.objects.get(u_id=c.form_uid)
        else:
            return 'id con\'t null'

    def commit_comment(self):
        try:
            c_commentdb = TbComment(form_uid=self.form_id, topic_id=self.topic_id, content=self.content)
            c_commentdb.save()
            return 'success'
        except:
            return 'database error'

    def commit_reply(self):
        try:
            c_replydb = TbReply(reply_id=self.reply_id, form_uid=self.form_uid, content=self.content)
            c_replydb.save()
            return 'success'
        except:
            return 'database error'
