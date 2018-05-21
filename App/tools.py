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