from rest_framework import serializers
from . import models

class RanklistSer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = 1
    
    id = serializers.SerializerMethodField()
    player = serializers.StringRelatedField(read_only=True,source='uname')
    rank = serializers.StringRelatedField(read_only=True,source='points')

    class Meta:
        model = models.BaseUser
        fields = "__all__"

    def get_id(self, obj):
        id = self.id
        self.id = id + 1
        return id


class RoomDetailSer(serializers.ModelSerializer):
    
    creater = serializers.SerializerMethodField()
    creatername = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    seats = serializers.SerializerMethodField()

    class Meta:
        model = models.RoomPlayer2Role
        fields = ("room_id","creater","creatername","status","seats")

    def get_creater(self, obj):
        roomid = obj.room_id
        roominfo = models.RoomInfo.objects.get(room_id=roomid)
        return roominfo.judge

    def get_status(self, obj):
        roomid = obj.room_id
        roominfo = models.RoomInfo.objects.get(room_id=roomid)
        return roominfo.status

    def get_creatername(self, obj):
        roomid = obj.room_id
        roominfo = models.RoomInfo.objects.get(room_id=roomid)
        uid = roominfo.judge
        creater = models.BaseUser.objects.get(uid=uid)
        return creater.uname

    def get_seats(self, obj):
        tempdict = {}
        for k in range(18):
            # 获取演员
            playernumber = "player" + str(k+1)
            playeruid = eval("obj." + playernumber)
            playername = None
            if playeruid:
                player = models.BaseUser.objects.get(uid=playeruid)
                playername = player.uname
            # 获取角色
            rolenumber = "role" + str(k+1)
            roleuid = eval("obj." + rolenumber)
            rolename = None
            if roleuid:
                role = models.BaseRoles.objects.get(role_id=roleuid)
                rolename = role.role_name
            # 写入临时字典
            tempdict[playernumber]= playername
            tempdict[rolenumber]= rolename
        return tempdict