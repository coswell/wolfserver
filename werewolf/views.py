# Create your views here.

from werewolf.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from werewolf.models import *

from django.core import serializers
import json,time

class login(APIView):

    # 登录检查 
    def get(self, request):
        userid = request.GET.get('user')
        user = BaseUser.objects.filter(uid=userid)
        if user:
            return Response(status=200)
        else:
            return Response(status=400)


class getRank(APIView):

    # 获取排行榜单
    def get(self, request):
        ranklist = BaseUser.objects.all().order_by('-points','-consumer')
        ranklist_ser = RanklistSer(ranklist,many=True)
        return Response(status=200,data=ranklist_ser.data)


class createRoom(APIView):

    # 创建一个状态为未开始的房间
    def post(self, request):
        gamingrooms = RoomInfo.objects.filter(status=0)
        if gamingrooms:
            gamingroom = gamingrooms[0]
            roomid = gamingroom.room_id
            errcode = 1
            creater = BaseUser.objects.get(uid=gamingroom.judge)
            res = {
                "errcode": errcode,
                "roomid": roomid,
                "creater": creater.uname
            }
        else:
            pdata = json.loads(request.body, encoding='utf-8')
            # print(pdata)
            roomid = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            roominfo = {
                "room_id":roomid,
                "status":0
                }
            for group,detail in pdata.items():
                if group == "configs": # 暂时跳过特殊规则的设置
                    for config,desc in detail.items():
                        tempdict = {config:desc["selected"]}
                        roominfo = dict(roominfo, **tempdict)
                elif group == "user":
                    tempdict = {"judge":detail}
                    roominfo = dict(roominfo, **tempdict)
                else:
                    for role,number in detail.items():
                        if role == "total":
                            continue
                        tempdict = {role:number}
                        roominfo = dict(roominfo, **tempdict)
            # print(roominfo)
            newroom = RoomInfo(**roominfo)
            newroom.save()
            errcode = 0
            res = {
                "errcode": errcode,
                "roomid": roomid
            }
        return Response(status=200, data=res)


class getRoomInfo(APIView):

    def get(self, request):
        userid = request.GET.get('user')
        roomid = request.GET.get('room')
        actuallyuser = BaseUser.objects.get(uid=userid)
        tempdict = {
            "selfname": actuallyuser.uname
        }
        room = RoomPlayer2Role.objects.get(room_id=roomid)
        selfcard,playernumber = self.getselfseatinfo(userid, room)
        tempdict["selfcard"] = selfcard
        tempdict["playernumber"] = playernumber
        room_ser = RoomDetailSer(room)
        return Response(status=200, data={**tempdict, **room_ser.data})

    def getselfcard(self, actuallyuser, obj):
        card = None
        for k in range(18):
            # 获取演员
            playernumber = "player" + str(k+1)
            playeruid = eval("obj." + playernumber)
            if actuallyuser == playeruid:
                # 获取角色
                rolenumber = "role" + str(k+1)
                roleuid = eval("obj." + rolenumber)
                rolename = None
                if roleuid:
                    role = BaseRoles.objects.get(role_id=roleuid)
                    rolename = role.role_description
                    card = rolename + '.jpg'
                break
        return (card,playernumber)

class seatAct(APIView):

    def get(self, request): #user,room,pre,to
        userid = request.GET.get('user')
        preseat = request.GET.get('pre')
        toseat = request.GET.get('to')
        roomid = request.GET.get('room')
        roominfo = RoomInfo.objects.get(room_id=roomid)
        room = RoomPlayer2Role.objects.get(room_id=roomid)
        roomptoseat = getattr(room,toseat)
        if roominfo.status != 0:
            res = {
                "errcode": 999,
                "msg": "游戏状态异常，不能入座/更换座位"
            }
        elif request.GET.get('type') == "0": # 入座
            if roomptoseat != None: # 检查座位是否有人
                res = {
                    "errcode": 1,
                    "msg": "该座位已经有人了！"
                }
            else:
                if preseat == '0' or not preseat : # 不需离座，直接入座
                    setattr(room, toseat, userid)
                    try:
                        room.save()
                        res = {
                            "errcode": 0,
                            "msg": "入座成功！"
                        }
                    except:
                        res = {
                            "errcode": 999,
                            "msg": "游戏状态异常，不能入座/更换座位"
                        }
                else: # 先离座，后入座
                    setattr(room, preseat, None)
                    setattr(room, toseat, userid)
                    try:
                        room.save()
                        res = {
                            "errcode": 0,
                            "msg": "入座成功！"
                        }
                    except:
                        res = {
                            "errcode": 999,
                            "msg": "游戏状态异常，不能入座/更换座位"
                        }
        else: # 离座
            setattr(room, preseat, None)
            try:
                room.save()
                res = {
                    "errcode": 0,
                    "msg": "离座成功！"
                }
            except:
                res = {
                    "errcode": 999,
                    "msg": "游戏状态异常，不能入座/更换座位"
                }
        return Response(status=200, data=res)