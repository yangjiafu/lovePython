# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from App.models import TbMovies, TbUsers, TbVideo
import json
import random


import Love.settings
import threading
import hashlib
import os

class AppConfig(AppConfig):
    name = 'App'


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
