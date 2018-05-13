# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TbComment(models.Model):
    c_id = models.AutoField(primary_key=True)
    topic_id = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=150, blank=True, null=True)
    form_uid = models.IntegerField(blank=True, null=True)
    form_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_comment'


class TbHotcomment(models.Model):
    h_id = models.AutoField(primary_key=True)
    h_uid = models.IntegerField(blank=True, null=True)
    h_comment = models.CharField(max_length=200, blank=True, null=True)
    h_time = models.DateTimeField()
    h_img = models.CharField(max_length=400, blank=True, null=True)
    h_video = models.CharField(max_length=50, blank=True, null=True)
    h_likes = models.CharField(max_length=1000, blank=True, null=True)
    h_like = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_hotcomment'


class TbHotreply(models.Model):
    hr_id = models.AutoField(primary_key=True)
    hr_uid = models.IntegerField(blank=True, null=True)
    hr_content = models.CharField(max_length=150, blank=True, null=True)
    hr_time = models.DateTimeField()
    hr_likes = models.CharField(max_length=1000, blank=True, null=True)
    hr_like = models.IntegerField(blank=True, null=True)
    hr_fromid = models.IntegerField(blank=True, null=True)
    hr_token = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_hotreply'


class TbMovies(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_name = models.CharField(max_length=50)
    m_othername = models.CharField(max_length=512, blank=True, null=True)
    m_cover = models.CharField(max_length=100, blank=True, null=True)
    m_actor = models.CharField(max_length=1024, blank=True, null=True)
    m_director = models.CharField(max_length=200, blank=True, null=True)
    m_classify = models.CharField(max_length=40, blank=True, null=True)
    m_area = models.CharField(max_length=20, blank=True, null=True)
    m_language = models.CharField(max_length=20, blank=True, null=True)
    m_releasetime = models.CharField(max_length=30, blank=True, null=True)
    m_duration = models.CharField(max_length=20, blank=True, null=True)
    m_score = models.CharField(max_length=10, blank=True, null=True)
    m_shortcomment = models.CharField(max_length=1024, blank=True, null=True)
    m_synopsis = models.CharField(max_length=2048, blank=True, null=True)
    m_linkinfo = models.CharField(db_column='m_linkInfo', max_length=3072)  # Field name made lowercase.
    m_info = models.CharField(max_length=1024, blank=True, null=True)
    m_userid = models.CharField(max_length=10, blank=True, null=True)
    m_plays = models.IntegerField(blank=True, null=True)
    m_like = models.IntegerField(blank=True, null=True)
    m_dislike = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_movies'


class TbReply(models.Model):
    r_id = models.AutoField(primary_key=True)
    reply_id = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=150, blank=True, null=True)
    form_uid = models.IntegerField(blank=True, null=True)
    form_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_reply'


class TbUsers(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=12)
    u_pwd = models.CharField(max_length=20, blank=True, null=True)
    u_gender = models.CharField(max_length=3, blank=True, null=True)
    u_age = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=50, blank=True, null=True)
    u_vip = models.IntegerField(blank=True, null=True)
    u_email = models.CharField(max_length=30)
    u_likemovies = models.CharField(max_length=30, blank=True, null=True)
    u_duration = models.CharField(max_length=4, blank=True, null=True)
    u_recording = models.CharField(max_length=30, blank=True, null=True)
    u_recommendmovie = models.CharField(db_column='u_recommendMovie', max_length=30, blank=True, null=True)  # Field name made lowercase.
    u_account = models.CharField(unique=True, max_length=20, blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)
    u_code = models.CharField(max_length=4, blank=True, null=True)
    u_ip = models.CharField(max_length=15, blank=True, null=True)
    u_avatar = models.CharField(max_length=50, blank=True, null=True)
    admin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_users'


class TbVideo(models.Model):
    v_path = models.CharField(max_length=30, blank=True, null=True)
    v_name = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tb_video'
