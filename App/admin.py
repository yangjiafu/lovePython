# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.conf import settings
from django.apps import AppConfig
from django.core.files import File
from App.models import TbMovies, TbUsers, TbVideo, TbReply, TbComment, TbHotcomment, TbHotreply
from App.tools import del_comment, del_hot_comment, del_hot_reply, del_reply, del_user, MovieForm, setpath, del_movie, is_admin
import Love.settings
import json
import time
import Love.settings
import threading
import hashlib
import os
import re


class Admin:
    def __init__(self, **kw):
        for k, w in kw.iteritems():
            setattr(self, k, w)

    def admin_login(self):
        str = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        if re.match(str, self.account):
            try:
                res = TbUsers.objects.get(u_email=self.account)
                if res.is_active == '1' and res.admin == '1':
                    if self.pwd == res.u_pwd:
                        tokens = hashlib.sha1(os.urandom(10)).hexdigest()
                        TbUsers.objects.filter(u_email=self.account).update(token=tokens)
                        s = {'id': res.u_id, 'avatar': res.u_avatar, 'name': res.u_name, 'email': res.u_email,
                             'vip': res.u_vip,
                             'token': tokens}
                        return json.dumps(s)
                    else:
                        return 'error'
                else:
                    return 'account error'
            except TbUsers.DoesNotExist:
                return 'not'
        else:
            try:
                res = TbUsers.objects.get(u_account=self.account)
                if res.is_active == '1' and res.admin == 1:
                    if self.pwd == res.u_pwd:
                        tokens = hashlib.sha1(os.urandom(24)).hexdigest()
                        TbUsers.objects.filter(u_account=self.account).update(token=tokens)
                        s = {'id': res.u_id, 'avatar': res.u_avatar, 'name': res.u_name, 'email': res.u_email,
                             'vip': res.u_vip,
                             'token': tokens}
                        return json.dumps(s)
                    else:
                        return 'error'
                else:
                    return 'notAdmin'
            except TbUsers.DoesNotExist:
                return 'not'

    def get_user(self):
        users = TbUsers.objects.order_by('-u_id')
        arr = []
        for u in users:
            res = {'name': u.u_name, 'id': u.u_id, 'active': u.is_active, 'email': u.u_email}
            arr.append(res)
        return json.dumps(arr)

    def del_user_info(self):
        try:
            token = TbUsers.objects.get(token=self.token)
            if token.u_id:
                if del_hot_reply('uid', self.id) and del_hot_comment('uid', self.id):
                    if del_reply('uid', self.id) and del_comment('uid', self.id):
                        if del_user(self.id):
                            return json.dumps('success')
                        else:
                            return json.dumps('delete user error')
                    else:
                        return json.dumps('delete comment error')
                else:
                    return json.dumps('delete hot error')
            else:
                return json.dumps('token error')
        except:
            return json.dumps('token error')

    def del_hot_comment(self):
        if del_hot_comment('cid', self.id):
            if del_hot_reply('cid', self.id):
                return json.dumps('success')
            else:
                return json.dumps('reply error')
        else:
            return json.dumps('comment error')

    def del_hot_reply(self):
        if del_hot_reply('hr_id', self.id):
            return json.dumps('success')
        else:
            return json.dumps('reply error')

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
            size = mf.cleaned_data['size']
            type = mf.cleaned_data['type']
            img = self.files.getlist('m_img')
            video = self.files.getlist('m_movie')
            try:
                img_path = setpath(img[0].name)
                img_des = open('./App/static/movies/img/' + img_path, 'wb+')
                for chunk in img[0].chunks():
                    img_des.write(chunk)
                img_des.close()
                video_path = setpath(video[0].name)
                video_des = open('./App/static/movies/video/' + video_path, 'wb+')
                for chunk in video[0].chunks():
                    video_des.write(chunk)
                video_des.close()
                video_path = '%s<<%s<<PATH_%s' % (size, type, video_path)
                img_path = 'PATH_%s' % img_path
                uploadMovie = TbMovies(m_name=movieName, m_othername=otherName, m_actor=actors, m_director=director,
                              m_classify=classify, m_area=area, m_language=language, m_releasetime=releasetime,
                              m_score=score, m_cover=img_path, m_linkinfo=video_path)
                uploadMovie.save()
                return json.dumps('success')
            except:
                return json.dumps('upload file error')
        else:
            return json.dumps('upload data error')

    def del_movies(self):
        if is_admin(self.token):
            if del_movie(self.id):
                return json.dumps('success')
            else:
                return json.dumps('del error')
        else:
            return json.dumps('token error')
