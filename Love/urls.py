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
# from django.contrib import admin
# from . import view
from App import views, admin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # url(r'^hello$', views.hello),
    url(r'^$', views.usersdb),
    # url(r'^admin/', admin.site.urls),
    url(r'^login$', views.user_login),
    url(r'^adminLogin$', views.admin_login),
    url(r'^deleteUser', views.delete_user),
    url(r'^delComment', views.delete_comment),
    url(r'deleteMovie', views.delete_movies),
    url(r'^editPwd$', views.edit_pwd),
    url(r'^tokenlogin', views.token_login),
    # url(r'^goEmail', views.doemail),
    url(r'^registered', views.registered),
    url(r'^getEmailCode', views.get_email_code),
    url(r'^getUsers', views.get_users),
    url(r'^searchMovie', views.search_movie),
    url(r'^uploadImg', views.upload_img),
    url(r'^uploadVideo', views.upload_video),
    url(r'^uploadMovie', views.upload_movie),
    url(r'^getComment', views.get_comment),
    url(r'^commitComment', views.commit_comment),
    url(r'^getNewMovie', views.get_movies),
    url(r'^goMovieLike', views.do_movie_like),
    url(r'^commitHotComment', views.commit_hot_comment),
    url(r'^commitHotFile', views.commit_hot_file),
    url(r'^commitHotReply', views.commit_hot_reply),
    url(r'^getHotComment', views.get_hot_comment),
    url(r'^doHotLike', views.do_comment_like),
    url(r'^static/(?P<path>.*)$', static)
]
