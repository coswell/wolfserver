# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BasePointLog(models.Model):
    roomid = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=255)
    pointtype = models.IntegerField()
    number = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_point_log'
        unique_together = (('roomid', 'user', 'pointtype'),)


class BaseRoles(models.Model):
    role_id = models.CharField(primary_key=True, max_length=32)
    role_name = models.CharField(max_length=255, blank=True, null=True)
    role_description = models.CharField(max_length=255, blank=True, null=True)
    role_group = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_roles'


class BaseUser(models.Model):
    uid = models.CharField(primary_key=True, max_length=255)
    uname = models.CharField(max_length=255, blank=True, null=True)
    points = models.FloatField(blank=True, null=True)
    consumer = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_user'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
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


class GameRoundInfo(models.Model):
    streamnumber = models.AutoField(primary_key=True)
    game_id = models.CharField(max_length=32, blank=True, null=True)
    game_rounds = models.IntegerField(blank=True, null=True)
    vote_id = models.IntegerField(blank=True, null=True)
    vote_id_second = models.IntegerField(blank=True, null=True)
    kill = models.CharField(max_length=255, blank=True, null=True)
    shooting = models.CharField(max_length=255, blank=True, null=True)
    poison = models.CharField(max_length=255, blank=True, null=True)
    cure = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_round_info'


class GameUserInfo(models.Model):
    game_id = models.CharField(primary_key=True, max_length=32)
    user_id = models.CharField(max_length=255)
    police = models.IntegerField(blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=4, blank=True, null=True)
    group = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_user_info'
        unique_together = (('game_id', 'user_id'),)


class GameVoteInfo(models.Model):
    vote_id = models.IntegerField(primary_key=True)
    voter = models.CharField(max_length=255, blank=True, null=True)
    vote4who = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_vote_info'


class PointLog(models.Model):
    room = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=2, blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'point_log'


class RoomInfo(models.Model):
    room_id = models.CharField(primary_key=True, max_length=32)
    judge = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    g_seer = models.IntegerField(blank=True, null=True)
    g_witch = models.IntegerField(blank=True, null=True)
    g_hunter = models.IntegerField(blank=True, null=True)
    g_savior = models.IntegerField(blank=True, null=True)
    g_idiot = models.IntegerField(blank=True, null=True)
    g_knight = models.IntegerField(blank=True, null=True)
    g_silence = models.IntegerField(blank=True, null=True)
    g_tombKeeper = models.IntegerField(blank=True, null=True)
    v_rogue = models.IntegerField(blank=True, null=True)
    v_villager = models.IntegerField(blank=True, null=True)
    w_whiteking = models.IntegerField(blank=True, null=True)
    w_blackking = models.IntegerField(blank=True, null=True)
    w_gargoyle = models.IntegerField(blank=True, null=True)
    w_wolfbeauty = models.IntegerField(blank=True, null=True)
    w_werewolf = models.IntegerField(blank=True, null=True)
    t_thief = models.IntegerField(blank=True, null=True)
    t_bomberman = models.IntegerField(blank=True, null=True)
    t_Cupid = models.IntegerField(blank=True, null=True)
    sheriff = models.IntegerField(blank=True, null=True)
    witch_save = models.IntegerField(blank=True, null=True)
    doublepills = models.IntegerField(blank=True, null=True)
    keepandsave = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_info'


class RoomPlayer2Role(models.Model):
    room_id = models.CharField(primary_key=True, max_length=32)
    player1 = models.CharField(max_length=255, blank=True, null=True)
    role1 = models.CharField(max_length=255, blank=True, null=True)
    player2 = models.CharField(max_length=255, blank=True, null=True)
    role2 = models.CharField(max_length=255, blank=True, null=True)
    player3 = models.CharField(max_length=255, blank=True, null=True)
    role3 = models.CharField(max_length=255, blank=True, null=True)
    player4 = models.CharField(max_length=255, blank=True, null=True)
    role4 = models.CharField(max_length=255, blank=True, null=True)
    player5 = models.CharField(max_length=255, blank=True, null=True)
    role5 = models.CharField(max_length=255, blank=True, null=True)
    player6 = models.CharField(max_length=255, blank=True, null=True)
    role6 = models.CharField(max_length=255, blank=True, null=True)
    player7 = models.CharField(max_length=255, blank=True, null=True)
    role7 = models.CharField(max_length=255, blank=True, null=True)
    player8 = models.CharField(max_length=255, blank=True, null=True)
    role8 = models.CharField(max_length=255, blank=True, null=True)
    player9 = models.CharField(max_length=255, blank=True, null=True)
    role9 = models.CharField(max_length=255, blank=True, null=True)
    player10 = models.CharField(max_length=255, blank=True, null=True)
    role10 = models.CharField(max_length=255, blank=True, null=True)
    player11 = models.CharField(max_length=255, blank=True, null=True)
    role11 = models.CharField(max_length=255, blank=True, null=True)
    player12 = models.CharField(max_length=255, blank=True, null=True)
    role12 = models.CharField(max_length=255, blank=True, null=True)
    player13 = models.CharField(max_length=255, blank=True, null=True)
    role13 = models.CharField(max_length=255, blank=True, null=True)
    player14 = models.CharField(max_length=255, blank=True, null=True)
    role14 = models.CharField(max_length=255, blank=True, null=True)
    player15 = models.CharField(max_length=255, blank=True, null=True)
    role15 = models.CharField(max_length=255, blank=True, null=True)
    player16 = models.CharField(max_length=255, blank=True, null=True)
    role16 = models.CharField(max_length=255, blank=True, null=True)
    player17 = models.CharField(max_length=255, blank=True, null=True)
    role17 = models.CharField(max_length=255, blank=True, null=True)
    player18 = models.CharField(max_length=255, blank=True, null=True)
    role18 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_player2role'


class WerewolfOutlog(models.Model):
    room = models.CharField(max_length=32)
    out = models.SmallIntegerField()
    stage = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'werewolf_outlog'


class WerewolfRooms(models.Model):
    room = models.CharField(max_length=32)
    stage = models.SmallIntegerField()
    canvote = models.SmallIntegerField()
    player = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'werewolf_rooms'


class WerewolfVotes(models.Model):
    candidate = models.SmallIntegerField()
    voter = models.SmallIntegerField()
    room = models.CharField(max_length=32)
    stage = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'werewolf_votes'
