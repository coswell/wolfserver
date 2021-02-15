# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

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
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=255, blank=True, null=True)
    role_description = models.CharField(max_length=255, blank=True, null=True)

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
    role1 = models.IntegerField(blank=True, null=True)
    role2 = models.IntegerField(blank=True, null=True)
    role3 = models.IntegerField(blank=True, null=True)
    role4 = models.IntegerField(blank=True, null=True)
    role5 = models.IntegerField(blank=True, null=True)
    role6 = models.IntegerField(blank=True, null=True)
    role7 = models.IntegerField(blank=True, null=True)
    role8 = models.IntegerField(blank=True, null=True)
    special_rule1 = models.IntegerField(blank=True, null=True)
    special_rule2 = models.IntegerField(blank=True, null=True)
    special_rule3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_info'


class RoomUser(models.Model):
    room_id = models.CharField(primary_key=True, max_length=32)
    user_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'room_user'
        unique_together = (('room_id', 'user_id'),)


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
