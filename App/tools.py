# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.http import HttpResponse
from App.models import TbMovies, TbUsers, TbVideo, TbReply, TbComment, TbHotcomment, TbHotreply
import os
# Create your tests here.


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


def del_hot_comment(id):
    try:
        hotComment = TbHotcomment.objects.filter(h_uid=id)
        for h in hotComment:
            file = 'App/static/hotComment/img/%s' % h.h_img
            if h.h_img and os.path.exists(file):
                os.remove(file)
        hotComment.delete()
        return True
    except:
        return False


def del_hot_reply(id):
    try:
        hotreply = TbHotreply.objects.filter(hr_uid=id)
        hotreply.delete()
        return True
    except:
        return False


def del_reply(id):
    try:
        reply = TbReply.objects.filter(form_uid=id)
        reply.delete()
        return True
    except:
        return False


def del_comment(id):
    try:
        comment = TbComment.objects.filter(form_uid=id)
        comment.delete()
        return True
    except:
        return False