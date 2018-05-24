# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.http import HttpResponse
from App.models import TbMovies, TbUsers, TbVideo, TbReply, TbComment, TbHotcomment, TbHotreply
import os
from django import forms
import time
import hashlib
import random
# Create your tests here.

_sysPath = 'http//:localhost:8000/'

def response_def(func):
    func = func
    return HttpResponse(func, content_type='application/json')


def del_user(id):
    try:
        user = TbUsers.objects.get(u_id=id)
        file = 'App/static/user/avatar/%s' % user.u_avatar
        if user.u_avatar and os.path.exists(file):
            os.remove(file)
        user.delete()
        return True
    except:
        return False


def del_hot_comment(type, id):
    try:
        if type == 'uid':
            hotComment = TbHotcomment.objects.filter(h_uid=id)
        else:
            hotComment = TbHotcomment.objects.filter(h_id=id)
        for h in hotComment:
            file = 'App/static/hotComment/img/%s' % h.h_img
            if h.h_img and os.path.exists(file):
                os.remove(file)
        hotComment.delete()
        return True
    except:
        return False


def del_hot_reply(type, id):
    try:
        if type == 'uid':
            hotreply = TbHotreply.objects.filter(hr_uid=id)
        elif type == 'cid':
            hotreply = TbHotreply.objects.filter(hr_fromid=id)
        else:
            hotreply = TbHotreply.objects.filter(hr_id=id)
        hotreply.delete()
        return True
    except:
        return False


def del_reply(type, id):
    try:
        if type == 'uid':
            reply = TbReply.objects.filter(form_uid=id)
        elif type == 'cid':
            reply = TbReply.objects.filter(reply_id=id)
        else:
            reply = TbReply.objects.filter(r_id=id)
        reply.delete()
        return True
    except:
        return False


def del_comment(type, id):
    try:
        if type == 'uid':
            comment = TbComment.objects.filter(form_uid=id)
        else:
            comment = TbComment.objects.filter(hr_id=id)
        comment.delete()
        return True
    except:
        return False


def del_movie(id):
    try:
        movie = TbMovies.objects.filter(m_id=id)
        for h in movie:
            path = h.m_linkinfo.split('<<')[2]
            v_file = 'App/static/movies/video/%s' % path.replace('PATH_', '')
            if os.path.exists(v_file):
                os.remove(v_file)
            i_file = 'App/static/movies/img/%s' % h.m_cover.replace('PATH_', '')
            if os.path.exists(i_file):
                os.remove(i_file)
        movie.delete()
        return True
    except:
        return False


def is_admin(token):
    try:
        token = TbUsers.objects.get(token=token)
        if token.token:
            return True
        else:
            return False
    except:
        return False


def setpath(name):
    fn = time.strftime('%Y%m%d%H%M%S')
    rd = random.randint(0, 100)
    rs = random.randint(0, 9)
    return '%s%s%s%s' % (fn, rs, rd, os.path.splitext(name)[1])


def send_email(username, mail):
    rs = random.sample('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 4)
    rs = ''.join(rs)
    msg = u'%s你好：<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;你的随机验证码为：' \
          u'<a style="color:red">%s</a><span style="font-size:10px">（忽略大小写）</span>' % (username, rs)
    send_mail(u'邮箱验证码', 'actions', settings.EMAIL_HOST_USER,
              [mail],
              html_message=msg
              )
    return rs


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
    size = forms.CharField()
    type = forms.CharField()
    # m_poster = forms.FileField()
    # m_movie = forms.FileField()