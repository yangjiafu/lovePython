"""Love URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# from . import view
from App import views

urlpatterns = [
    # url(r'^hello$', views.hello),
    url(r'^$', views.usersdb),
    url(r'^admin/', admin.site.urls),
    url(r'^login$', views.user_login),
    url(r'^editPwd$', views.edit_pwd),
    url(r'^tokenlogin', views.token_login),
    # url(r'^goEmail', views.doemail),
    url(r'^registered', views.registered),
    url(r'^getEmailCode', views.get_email_code),
    url(r'^searchMovie', views.search_movie),
    url(r'^uploadImg', views.upload_img),
    url(r'^uploadVideo', views.upload_video),
    url(r'^uploadMovie', views.upload_movie),
    url(r'^getComment', views.get_comment),
    url(r'^commitComment', views.commit_comment),

]
