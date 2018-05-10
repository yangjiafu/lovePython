# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.apps import AppConfig
from django.core.files import File
from App.models import TbMovies, TbUsers, TbVideo, TbReply, TbComment, TbHotcomment, TbHotreply
import json
import random
import re
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


class UserForm(forms.Form):
    account = forms.CharField()
    username = forms.CharField()
    pwd = forms.CharField()
    email = forms.CharField()
    # gender = forms.CharField()
    # age = forms.CharField()
    # avatar = forms.FileField()


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


def detection(account, type):
    if type == 'email':
        try:
            info = TbUsers.objects.get(u_email=account)
            if info.is_active != '1':
                TbUsers.objects.filter(u_email=account).delete()
            else:
                pass
        except TbUsers.DoesNotExist:
            pass
    else:
        try:
            info = TbUsers.objects.get(u_account=account)
            if info.is_active != '1':
                TbUsers.objects.filter(u_account=account).delete()
            else:
                pass
        except TbUsers.DoesNotExist:
            pass


def push_movie(m):
    arr = []
    for i in m:
        ins = {'id': i.m_id, 'name': i.m_name, 'cover': File(i.m_cover).name, 'score': i.m_score}
        arr.append(ins)
    return arr


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
        str = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        if re.match(str, self.account):
            try:
                res = TbUsers.objects.get(u_email=self.account)
                if self.pwd == res.u_pwd:
                    tokens = hashlib.sha1(os.urandom(10)).hexdigest()
                    TbUsers.objects.filter(u_email=self.account).update(token=tokens)
                    s = {'id': res.u_id, 'pwd': res.u_pwd, 'name': res.u_name, 'email': res.u_email, 'vip': res.u_vip,
                         'token': tokens}
                    return json.dumps(s)
                else:
                    return 'error'
            except TbUsers.DoesNotExist:
                return 'not'
        else:
            try:
                res = TbUsers.objects.get(u_account=self.account)
                if self.pwd == res.u_pwd:
                    tokens = hashlib.sha1(os.urandom(24)).hexdigest()
                    TbUsers.objects.filter(u_account=self.account).update(token=tokens)
                    s = {'id': res.u_id, 'pwd': res.u_pwd, 'name': res.u_name, 'email': res.u_email, 'vip': res.u_vip,
                         'token': tokens}
                    return json.dumps(s)
                else:
                    return 'error'
            except TbUsers.DoesNotExist:
                return 'not'

    def user_get_code(self):
        uf = UserForm(self.post, self.files)
        if uf.is_valid():
            account = uf.cleaned_data['account']
            username = uf.cleaned_data['username']
            pwd = uf.cleaned_data['pwd']
            email = uf.cleaned_data['email']
            # gender = uf.cleaned_data['gender']
            # age = uf.cleaned_data['age']
            # avatar = uf.cleaned_data['avatar']
            try:
                TbUsers.objects.get(u_account=account)
                return u'have account'
            except TbUsers.DoesNotExist:
                try:
                    TbUsers.objects.get(u_email=email)
                    return u'have email'
                except TbUsers.DoesNotExist:
                    code = send_email(username, email)
                    # tbuser = TbUsers(u_account=account, u_name=username, u_pwd=pwd, u_email=email, u_code=code, u_avatar=avatar)
                    tbuser = TbUsers(u_account=account, u_name=username, u_pwd=pwd, u_email=email, u_code=code)
                    tbuser.save()
                    # 60s后检测是否注册成功，如果未注册则删除此条记录
                    change = threading.Timer(61.0, detection, (account, 'account'))
                    change.start()
                    return 'buffer'
        else:
            print 'error'

    def user_get_pcode(self):
        name = self.name
        email = self.email
        pwd = self.pwd
        try:
            TbUsers.objects.get(u_email=email)
            return 'have email'
        except TbUsers.DoesNotExist:
            code = send_email(name, email)
            # tbuser = TbUsers(u_account=account, u_name=username, u_pwd=pwd, u_email=email, u_code=code, u_avatar=avatar)
            tbuser = TbUsers(u_name=name, u_pwd=pwd, u_email=email, u_code=code, is_active=0)
            tbuser.save()
            # 60s后检测是否注册成功，如果未注册则删除此条记录
            change = threading.Timer(61.0, detection, (email, 'email'))
            change.start()
            return 'buffer'

    def user_register(self):
        str = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        dates = self.account
        if re.match(str, dates):
            try:
                info = TbUsers.objects.get(u_email=dates)
                print info.u_code.lower(), self.code.lower(), info.is_active
                if info.u_code.lower() == self.code.lower() and info.is_active != '1':
                    TbUsers.objects.filter(u_email=dates).update(is_active='1')
                    print 'success'
                    return 'is success'
                else:
                    print 'err'
                    return 'code err'
            except TbUsers.DoesNotExist:
                return 'not email'
        else:
            try:
                info = TbUsers.objects.get(u_account=dates)
                if info.u_code.lower() == self.code.lower() and info.is_active != '1':
                    TbUsers.objects.filter(u_account=dates).update(is_active='1')
                    return 'is success'
                else:
                    return 'code err'
            except TbUsers.DoesNotExist:
                return 'not account'

    def user_token_login(self):
        try:
            res = TbUsers.objects.get(u_id=self.id)
            if res.token == self.token:
                s = {'id': res.u_id, 'name': res.u_name, 'email': res.u_email, 'vip': res.u_vip,
                     'token': res.token}
                return json.dumps(s)
            else:
                return 'token err'
        except TbUsers.DoesNotExist:
            return 'login error'

    def user_edit_getcode(self):
        str = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        dates = self.dates
        if re.match(str, dates):
            try:
                TbUsers.objects.get(u_email=dates)
                code = send_email('', dates)
                TbUsers.objects.filter(u_email=dates).update(u_code=code)
                return 'success'
            except TbUsers.DoesNotExist:
                return 'not email'
        else:
            try:
                res = TbUsers.objects.get(u_account=dates)
                code = send_email(res.u_name, res.u_email)
                TbUsers.objects.filter(u_account=dates).update(u_code=code)
                return 'success'
            except TbUsers.DoesNotExist:
                return 'not account'

    def user_edit_pwd(self):
        str = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        dates = self.dates
        pwd = self.pwd
        code = self.code
        if re.match(str, dates):
            try:
                res = TbUsers.objects.get(u_email=dates)
                if res.u_code.lower() == code.lower():
                    try:
                        TbUsers.objects.filter(u_email=dates).update(u_pwd=pwd)
                        return 'success'
                    except:
                        return 'pwd error'
                else:
                    return 'code error'
            except TbUsers.DoesNotExist:
                return 'not'
        else:
            try:
                res = TbUsers.objects.get(u_account=dates)
                if res.u_code.lower() == code.lower():
                    try:
                        TbUsers.objects.filter(u_account=dates).update(u_pwd=pwd)
                        return 'success'
                    except:
                        return 'pwd error'
                else:
                    return 'code error'
            except TbUsers.DoesNotExist:
                return 'not'

    def user_like_movie(self):
        # try:
        # m_id = int(self.m_id)
        # u_id = int(self.u_id)
        user = TbUsers.objects.get(u_id=self.u_id)
        u_like = user.u_likemovies if user.u_likemovies else ''
        havaId = False
        for u in u_like.split(','):
            if u == self.m_id:
                havaId=True
                break
        if havaId:
            movie = TbMovies.objects.get(m_id=self.m_id)
            TbMovies.objects.filter(m_id=self.m_id).update(m_like=movie.m_like-1)
            print user.u_likemovies.replace(self.m_id+',', '')
            u_likemovies = '%s' % (user.u_likemovies.replace(self.m_id, '').lstrip(',').rstrip(','))
            TbUsers.objects.filter(u_id=self.u_id).update(u_likemovies=u_likemovies)
            # user.u_likemovies('%s,' % (user.u_likemovies.replace(self.m_id+',', '')))
            # user.save()
            return 'sub'
        else:
            movie = TbMovies.objects.get(m_id=self.m_id)
            TbMovies.objects.filter(m_id=self.m_id).update(m_like=movie.m_like+1)
            print 'else: ', u_like, self.m_id
            if len(u_like) < 1:
                TbUsers.objects.filter(u_id=self.u_id).update(u_likemovies=self.m_id)
                # user.u_likemovies('%s,' % self.m_id)
            else:
                u_likemovies = '%s,%s,' % (u_like, self.m_id)
                TbUsers.objects.filter(u_id=self.u_id).update(u_likemovies=u_likemovies.lstrip(',').rstrip(','))
                # user.u_likemovies('%s,%s,' % (u_like, self.m_id))
            return 'add'
        # except:
        #     return 'error'


class Search:
    def __init__(self, **kw):
        for k, w in kw.iteritems():
            setattr(self, k, w)

    def search_movie(self):
        try:
            movie = self.movie
            if len(movie) > 0:
                userid = TbUsers.objects.get(u_id=self.u_id)
                # print userid.u_likemovies
                # userid.u_likemovies = userid.u_likemovies if userid.u_likemovies else ''
                if self.type == 'name':
                    movies = TbMovies.objects.filter(m_name__contains=movie)
                else:
                    movies = TbMovies.objects.filter(m_id=movie)
                info = []
                for i in movies:
                    islike = 0
                    # if len(userid.u_likemovies) > 0:
                    if userid.u_likemovies == 'None':
                        for u in userid.u_likemovies.split(','):
                            if u == self.movie:
                                islike = 1
                                break
                    ins = {'id': i.m_id, 'name': i.m_name, 'othername': i.m_othername, 'cover': File(i.m_cover).name, 'actor': i.m_actor, 'director': i.m_director, 'classify': i.m_classify, 'area': i.m_area, 'language': i.m_language,
                           'releasetime': i.m_releasetime, 'duration': i.m_duration, 'score': i.m_score, 'synopsis': i.m_synopsis, 'linkInfo': File(i.m_linkinfo).name, 'like': i.m_like, 'dislike': i.m_dislike, 'islike': islike}
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
            upData = TbMovies(m_name=movieName, m_othername=otherName, m_actor=actors, m_director=director,
                              m_classify=classify, m_area=area, m_language=language, m_releasetime=releasetime,
                              m_score=score, m_cover=m_poster, m_linkinfo=m_movie)
            upData.save()
            return 'upload success!!'
        else:
            return 'the data have wrong'

    def movies(self):
        if self.place == 'home':
            movies = {'new': [], 'comedy': [], 'action': [],  'fantasy': [], 'war': []}
            newmovie = TbMovies.objects.order_by('-m_id')[0:4]
            movies['new'] = push_movie(newmovie)
            comedymovie = TbMovies.objects.filter(m_classify__contains=u'喜剧')[0:5]
            movies['comedy'] = push_movie(comedymovie)
            actionmovie = TbMovies.objects.filter(m_classify__contains=u'动作')[0:5]
            movies['action'] = push_movie(actionmovie)
            fantasymovie = TbMovies.objects.filter(m_classify__contains=u'奇幻')[0:5]
            movies['fantasy'] = push_movie(fantasymovie)
            warmovie = TbMovies.objects.filter(m_classify__contains=u'战争')[0:5]
            movies['war'] = push_movie(warmovie)
            return json.dumps(movies)
        else:
            pass
            # for i in movies:
            #     ins = {'id': i.m_id, 'name': i.m_name, 'othername': i.m_othername, 'cover': File(i.m_cover).name, 'actor': i.m_actor,
            #            'director': i.m_director, 'classify': i.m_classify, 'area': i.m_area, 'language': i.m_language,
            #            'releasetime': i.m_releasetime, 'duration': i.m_duration, 'score': i.m_score,
            #            'synopsis': i.m_synopsis, 'linkInfo': File(i.m_linkinfo).name}
            #     info.append(ins)


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
                show_reply = True if len(replys) > 0 else False
                cins = {'c_id': c.c_id, 'content': c.content, 'topic_id': c.topic_id, 'form_uid': c.form_uid,
                        'form_name': user.u_name, 'form_avatar': form_c_avatar, 'reply': replys, 'show_reply': show_reply}
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

    def commit_hot_comment(self):
        try:
            c_h_c = TbHotcomment(h_uid=self.h_uid, h_comment=self.h_comment, h_like=0, h_likes='')
            c_h_c.save()
            return 'success'
        except:
            return 'error'

    def commit_hot_reply(self):
        try:
            c_h_r = TbHotreply(hr_uid=self.hr_uid, hr_content=self.hr_content, hr_fromid=self.hr_fromid, hr_like=0, hr_likes='')
            c_h_r.save()
            return 'success'
        except:
            return 'error'

    def get_hot_comment(self):
        # try:
        hotcomment = TbHotcomment.objects.order_by('-h_id')[self.start:self.limit]
        comments = []
        if len(hotcomment) > 0:
            for c in hotcomment:
                reply = TbHotreply.objects.filter(hr_fromid=c.h_id)
                cuser = TbUsers.objects.get(u_id=c.h_uid)
                imgpath = File(c.h_img).name if c.h_img else ''
                videopath = File(c.h_video).name if c.h_video else ''
                avatarPath = File(cuser.u_avatar).name if cuser.u_avatar else ''
                isLike = False
                if c.h_likes:
                    for uid in c.h_likes.split(','):
                        if uid == self.hr_uid:
                            isLike = True
                            break
                ccomment = {'name': cuser.u_name, 'id': cuser.u_id, 'avatar': avatarPath, 'isLike': isLike,
                            'comment': c.h_comment, 'img': imgpath, 'video': videopath, 'like': c.h_like,
                            'replay': []}
                for r in reply:
                    ureply = TbUsers.objects.get(u_id=r.hr_uid)
                    rimgPath = File(ureply.u_avatar).name if ureply.u_avatar else ''
                    isRlike = False
                    if r.hr_likes:
                        for urId in r.hr_likes.split(','):
                            if urId == self.hr_uid:
                                isRlike = True
                                break
                    repcontent = {'name': ureply.u_name, 'id': ureply.u_id, 'avatar': rimgPath, 'isLike': isRlike,
                                  'comment': r.hr_content}
                    ccomment['replay'].append(repcontent)
                comments.append(ccomment)
            return json.dumps(comments)
        # except:
        #     return 'error'