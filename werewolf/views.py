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

    def get(self, request): # user,room
        userid = request.GET.get('user')
        roomid = request.GET.get('room')
        actuallyuser = BaseUser.objects.get(uid=userid)
        tempdict = {
            "selfname": actuallyuser.uname
        }
        room = RoomPlayer2Role.objects.get(room_id=roomid)
        selfcard,playernumber = self.getselfinfo(userid, room)
        tempdict["selfcard"] = selfcard
        tempdict["playernumber"] = playernumber
        room_ser = RoomDetailSer(room)
        return Response(status=200, data={**tempdict, **room_ser.data})

    def getselfinfo(self, actuallyuser, obj):
        card = None
        playernumber = None
        for k in range(18):
            # 获取演员
            player = "player" + str(k+1)
            playeruid = getattr(obj,player)
            if actuallyuser == playeruid:
                playernumber = k+1
                # 获取角色
                rolenumber = "role" + str(k+1)
                roleuid = getattr(obj,rolenumber)
                rolename = None
                if roleuid:
                    role = BaseRoles.objects.get(role_id=roleuid)
                    rolename = role.role_description
                    card = rolename + '.jpg'
                break
        return (card,playernumber)


class findRoom(APIView):
    def get(self, request):
        room = RoomInfo.objects.filter(status__in=[0,1])
        if not room:
            res = {
                "errcode": 2,
                "msg": "暂无可加入房间"
            }
        else:
            res = {
                "errcode": 0,
                "roomid": room[0].room_id,
                "judge": room[0].judge,
                "msg": "加入成功！"
            }
        return Response(status=200, data=res)


class seatAct(APIView):

    def get(self, request): # user,room,pre,to,type
        userid = request.GET.get('user')
        roomid = request.GET.get('room')
        roominfo = RoomInfo.objects.get(room_id=roomid)
        room = RoomPlayer2Role.objects.get(room_id=roomid)
        if roominfo.status != 0:
            res = {
                "errcode": 999,
                "msg": "游戏状态异常，不能入座/更换座位"
            }
        elif request.GET.get('type') == "0": # 入座
            toseat = request.GET.get('to')
            roomptoseat = getattr(room,toseat)
            if roomptoseat != None: # 检查座位是否有人
                res = {
                    "errcode": 1,
                    "msg": "该座位已经有人了！"
                }
            else:
                preseatnumber = request.GET.get('pre')
                if preseatnumber == '0' or not preseatnumber : # 不需离座，直接入座
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
                    preseat = "player" + request.GET.get('pre')
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
            preseat = "player" + request.GET.get('pre')
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


class getSelfInfoandRoomRoles(APIView):
    def get(self, request): # user,room
        userid = request.GET.get("user")
        roomid = request.GET.get("room")
        # 先获取个人信息 - 姓名和消费积分
        user = BaseUser.objects.get(uid=userid)
        username = user.uname
        cpoint = user.consumer
        res = {
            "selfname": username,
            "selfpoint": cpoint
        }
        roomconf = RoomInfo.objects.get(room_id=roomid)
        roleslist = {}
        for field in roomconf._meta.fields:
            name = field.attname    # 获取字段名
            value = getattr(roomconf, name)    #获取对象属性
            if name[:2] not in ("g_","v_","w_","t_"):
                continue
            if value > 0:
                role = BaseRoles.objects.get(role_id=name)
                # roleslist.append({name:role.role_description})
                roleslist[name] = role.role_description
        res["roleslist"] = roleslist
        return Response(status=200,data=res)


class preSelected(APIView):
    def get(self, request): # user,room,role
        userid = request.GET.get("user")
        roomid = request.GET.get("room")
        roleid = request.GET.get("role")
        res = {
            "errcode":0
        }
        # 检查房间状态
        room = RoomInfo.objects.get(room_id=roomid)
        if room.status == 0:
            selected = RoomRolePreselection.objects.filter(room_id=roomid,user=userid)
            if selected:
                selected[0].role = roleid
                selected[0].save()
            else:
                selectedconf = {
                    "room_id": roomid,
                    "user": userid,
                    "role": roleid
                }
                selected = RoomRolePreselection(**selectedconf)
                selected.save()
        else:
            res["errcode"] = 1
        return Response(status=200,data=res)