# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.conf import settings
from django.apps import AppConfig
from django.core.files import File
from App.models import TbMovies, TbUsers, TbVideo, TbReply, TbComment, TbHotcomment, TbHotreply
from App.tools import del_comment, del_hot_comment, del_hot_reply, del_reply, del_user
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
                if del_hot_reply(self.id) and del_hot_comment(self.id):
                    if del_reply(self.id) and del_comment(self.id):
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


