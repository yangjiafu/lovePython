# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# encoding: utf-8
import json
import random
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from App.models import TbMovies, TbUsers, TbVideo
from App.apps import User, Search, Movies, Comment
from django.conf import settings
from django.core.mail import send_mail
# 上传图片添加项
from django import forms
from django.shortcuts import render
import Image

import Love.settings
import threading
import hashlib
import os


def response_def(func):
    func = func
    return HttpResponse(func, content_type='application/json')


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
def get_email_code(request):
    if request.POST:
        if request.content_type == 'multipart/form-data':
            u_fcode = User(post=request.POST, files=request.FILES)
            return response_def(u_fcode.user_get_code())
            # u_code = User(account=request.POST['account'], name=request.POST['name'], pwd=request.POST['pwd'],
            #               email=request.POST['email'], gender=request.POST['gender'], age=request.POST['age'])
            # return response_def(u_code.user_get_code())
        else:
            u_pcode = User(name=request.POST['name'], email=request.POST['email'], pwd=request.POST['pwd'])
            return response_def(u_pcode.user_get_pcode())


@csrf_exempt
def registered(request):
    if request.POST:
        u_register = User(account=request.POST['account'], code=request.POST['code'])
        return response_def(u_register.user_register())


@csrf_exempt
def user_login(request):
    if request.POST:
        u_login = User(account=request.POST['account'], pwd=request.POST['pwd'])
        return response_def(u_login.user_login())
    else:
        return response_def('not support get submit')


@csrf_exempt
def token_login(request):
    if request.POST:
        u_token_login = User(token=request.POST['token'], id=request.POST['id'])
        return response_def(u_token_login.user_token_login())


@csrf_exempt
def edit_pwd(request):
    if request.POST:
        if request.POST['type'] == 'getcode':
            u_edit_code = User(dates=request.POST['date'])
            return response_def(u_edit_code.user_edit_getcode())
        else:
            u_edit_pwd = User(dates=request.POST['date'], pwd=request.POST['pwd'], code=request.POST['code'])
            return response_def(u_edit_pwd.user_edit_pwd())


@csrf_exempt
def search_movie(request):
    if request.GET:
        s_movie = Search(movie=request.GET['movie'], type=request.GET['type'], u_id=request.GET['u_id'])
        return response_def(s_movie.search_movie())
    else:
        return response_def('not support get submit')


@csrf_exempt
def get_movies(request):
    if request.GET:
        movie = Movies(start=request.GET['start'], limit=request.GET['limit'], place=request.GET['place'])
        return response_def(movie.movies())


@csrf_exempt
def upload_img(request):
    if request.method == 'POST':
        # return HttpResponse('upload success %s' % request.POST['name'])
        photo = request.FILES['uploadFile']
        if photo:
            photoname = '%s' % (photo._name)
            img = Image.open(photo)
            img.save(photoname)
            return HttpResponse('upload success %s' % request.POST['name'])
        else:
            return HttpResponse('upload error')


class UserForm(forms.Form):
    username = forms.CharField()
    headVideo = forms.FileField()

# class MovieForm(forms.Form):
#     movieName = forms.CharField()
#     otherName = forms.CharField()
#     actors = forms.CharField()
#     director = forms.CharField()
#     classify = forms.CharField()
#     area = forms.CharField()
#     language = forms.CharField()
#     releasetime = forms.CharField()
#     score = forms.CharField()
#     m_poster = forms.FileField()
#     m_movie = forms.FileField()
#

@csrf_exempt
def upload_movie(request):
    if request.method == 'POST':
        m_upload_movie = Movies(post=request.POST, files=request.FILES)
        return response_def(m_upload_movie.upload_movie())
        # mf = MovieForm(request.POST, request.FILES)
        # if mf.is_valid():
        #     movieName = mf.cleaned_data['movieName']
        #     otherName = mf.cleaned_data['otherName']
        #     actors = mf.cleaned_data['actors']
        #     director = mf.cleaned_data['director']
        #     classify = mf.cleaned_data['classify']
        #     area = mf.cleaned_data['area']
        #     language = mf.cleaned_data['language']
        #     releasetime = mf.cleaned_data['releasetime']
        #     score = mf.cleaned_data['score']
        #     m_poster = mf.cleaned_data['m_poster']
        #     m_movie = mf.cleaned_data['m_movie']
        #     print movieName
        #     upData = TbMovies(m_name=movieName, m_othername=otherName, m_actor=actors, m_director=director,
        #                       m_classify=classify, m_area=area, m_language=language, m_releasetime=releasetime,
        #                       m_score=score, m_cover=m_poster, m_linkinfo=m_movie)
        #     upData.save()
        #     print u'上传成功'
        #     return HttpResponse('upload success!!')


@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, request.FILES)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            headVideo = uf.cleaned_data['headVideo']
            uploadFile = TbVideo()
            uploadFile.v_name = username
            uploadFile.v_path = headVideo
            uploadFile.save()
            return HttpResponse('upload success!%s' % username)
        else:
            return HttpResponse('upload error')


@csrf_exempt
def get_comment(request):
    if request.GET:
        g_comment = Comment(id=request.GET['m_id'])
        return response_def(g_comment.get_comment())


@csrf_exempt
def commit_comment(request):
    if request.method == 'POST':
        if request.POST['type'] == 'comment':
            c_comment = Comment(form_id=request.POST['form_id'], topic_id=request.POST['topic_id'],
                                content=request.POST['content'])
            return response_def(c_comment.commit_comment())
        else:
            c_reply = Comment(form_uid=request.POST['form_uid'], reply_id=request.POST['reply_id'],
                              content=request.POST['content'])
            return response_def(c_reply.commit_reply())


@csrf_exempt
def do_movie_like(request):
    if request.POST:
        like_movie = User(u_id=request.POST['u_id'], m_id=request.POST['m_id'])
        return response_def(like_movie.user_like_movie())


@csrf_exempt
def commit_hot_comment(request):
    if request.POST:
        if request.POST['type'] == 'comment':
            hot_comment = Comment(h_uid=request.POST['h_uid'], h_comment=request.POST['h_comment'])
            return response_def(hot_comment.commit_hot_comment())


@csrf_exempt
def commit_hot_reply(request):
    if request.POST:
        hot_reply = Comment(hr_uid=request.POST['hr_uid'], hr_content=request.POST['hr_content'], hr_fromid=request.POST['hr_fromid'])
        return response_def(hot_reply.commit_hot_reply())


@csrf_exempt
def get_hot_comment(request):
    if request.GET:
        if request.GET['type'] == 'comment':
            hot_comments = Comment(u_id=request.GET['u_id'], limit=request.GET['limit'], start=request.GET['start'])
            return response_def(hot_comments.get_hot_comment())
        else:
            hot_replys = Comment(u_id=request.GET['u_id'], limit=request.GET['limit'], start=request.GET['start'],
                                 hr_formId=request.GET['hr_formId'])
            return response_def(hot_replys.get_hot_replys())


@csrf_exempt
def do_comment_like(request):
    if request.POST:
        if request.POST['type'] == 'comment':
            comment_like = Comment(u_id=request.POST['u_id'], comment_id=request.POST['comment_id'])
            return response_def(comment_like.do_comment_like())
        elif request.POST['type'] == 'reply':
            reply_like = Comment(u_id=request.POST['u_id'], reply_id=request.POST['reply_id'])
            return response_def(reply_like.do_reply_like())
