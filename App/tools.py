# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.http import HttpResponse
# Create your tests here.


def response_def(func):
    func = func
    return HttpResponse(func, content_type='application/json')