# Create your views here.

from werewolf.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from werewolf.models import *

from django.core import serializers
import json,time,random

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
        gamingrooms = RoomInfo.objects.filter(status__in=[0,1])
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
            newplayer2role = RoomPlayer2Role(room_id=roomid)
            newplayer2role.save()
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
                    rolename = role.role_name
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
                roleslist[name] = role.role_name
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


class divCard(APIView):
    def get(self, request): # user, room
        userid = request.GET.get("user")
        roomid = request.GET.get("room")
        pointloglist = []
        res = {
            "errcode": 0
        }
        # 检查房间状态
        room = RoomInfo.objects.get(room_id=roomid)
        if room.status != 0:
            res["errcode"] = 1
            res["msg"] = "该局游戏已经发过牌了"
        elif userid != room.judge:
            res["errcode"] = 2
            res["msg"] = "你不是该局游戏的创建人！"
        else:
            # 角色表
            player2role = {}
            # 表头映射表
            headmapping = {
                "g_": "god",
                "v_": "villagers",
                "w_": "wolf",
                "t_": "third"
            }

            # 生成角色池
            roomconf = RoomInfo.objects.get(room_id=roomid)
            rolespool = {
                "god": [],
                "villagers": [],
                "wolf": [],
                "third": [],
                "total": []
            }
            for field in roomconf._meta.fields:
                roleid = field.attname    # 获取字段名
                number = getattr(roomconf, roleid)    #获取对象属性
                if roleid[:2] not in ("g_","v_","w_","t_"):
                    continue
                while number > 0:
                    rolespool[headmapping[roleid[:2]]].append(roleid)
                    rolespool["total"].append(roleid)
                    number -= 1

            # 生成选手池(key->user, value->playerxx)
            roomseats = RoomPlayer2Role.objects.get(room_id=roomid)
            # 先获取总人数
            playerspool = {}
            totalroles = 18
            # for group,rolelist in rolespool.items():
            #     if group == "total":
            #         continue
            #     totalroles = totalroles + len(rolelist)
            for i in range(totalroles):
                seat = "player" + str(i+1)
                if getattr(roomseats,seat):
                    playerspool[getattr(roomseats,seat)] = seat
            
            # 遍历预选
            preselectionlist = {
                "role": {},
                "not_god": [],
                "not_wolf": [],
                "not_villagers": []
            }
            preselections = RoomRolePreselection.objects.filter(room_id=roomid)
            if preselections: # 若有预选则先处理预选
                for preselection in preselections:
                    player = preselection.user
                    role = preselection.role
                    if role[:3] == "not":
                        preselectionlist[role].append(player)
                    else:
                        if preselectionlist["role"].get(role):
                            preselectionlist["role"][role].append(player)
                        else:
                            preselectionlist["role"][role]=[player,]
                # 先处理role
                for roleid,userlist in preselectionlist["role"].items():
                    rolegroup = headmapping[roleid[:2]]
                    if rolegroup == "villagers" or rolegroup == "wolf":
                        rolesnumber = len(rolespool[rolegroup])
                    else:
                        rolesnumber = 1
                    tempuserlist = userlist
                    for i in range(rolesnumber):
                        luckyuser = random.choice(tempuserlist) # 随机选一个
                        luckyseat = playerspool.get(luckyuser) # 取得座位号
                        tempuserlist.remove(luckyuser)
                        if luckyseat: # 已经入座才算
                            if roleid in rolespool["total"]: # 池子里还有才算
                                player2role[luckyseat] = roleid # 写入玩家角色映射表{playerxx: roleid}
                                rolespool[rolegroup].remove(roleid) # 移除角色池里对应角色
                                rolespool["total"].remove(roleid) # 移除总角色池里对应角色
                                playerspool.pop(luckyuser) # 移除选手池里对应玩家
                                roleinfo = BaseRoles.objects.get(role_id=roleid)
                                pointlog = PointLog(
                                    room=roomid,
                                    type="2",
                                    uid=luckyuser,
                                    desc="购买指定角色卡(%s)"%(roleinfo.role_description),
                                    number=-12
                                    )
                                pointloglist.append(pointlog)
                        if not tempuserlist:
                            break
                # 然后处理非神
                temprolelist = [*rolespool["villagers"],*rolespool["wolf"],*rolespool["third"]] # 临时角色池
                userlist = preselectionlist["not_god"] # 预选非神玩家池
                if userlist:
                    for i in range(len(temprolelist)):
                        luckyrole = random.choice(tempuserlist)
                        luckyuser = random.choice(userlist)
                        luckyseat = playerspool.get(luckyuser) # 取得座位号
                        playerspool.pop(luckyuser) # 移除选手池里对应玩家
                        if luckyseat: # 入座才算
                            player2role[luckyseat] = roleid # 写入玩家角色映射表
                            userlist.remove(luckyuser) # 移除预选非神玩家池里对应的玩家
                            rolegroup = headmapping[luckyrole[:2]]
                            rolespool[rolegroup].remove(luckyrole) # 移除角色池里对应角色
                            rolespool["total"].remove(luckyrole) # 移除总角色池里对应角色
                            temprolelist.remove(luckyrole) # 移除临时角色池里对应的角色
                            roleinfo = BaseRoles.objects.get(role_id=luckyrole)
                            pointlog = PointLog(
                                        room=roomid,
                                        type="2",
                                        uid=luckyuser,
                                        desc="购买指定角色卡(%s)"%(roleinfo.role_description),
                                        number=-3 # 非神3分
                                        )
                            pointloglist.append(pointlog)
                        if not userlist:
                            break

                # 然后处理非民
                temprolelist = [*rolespool["god"],*rolespool["wolf"],*rolespool["third"]] # 临时角色池
                userlist = preselectionlist["not_villagers"] # 预选非神玩家池
                if userlist:
                    for i in range(len(temprolelist)):
                        luckyrole = random.choice(tempuserlist)
                        luckyuser = random.choice(userlist)
                        luckyseat = playerspool.get(luckyuser) # 取得座位号
                        playerspool.pop(luckyuser) # 移除选手池里对应玩家
                        if luckyseat: # 入座才算
                            player2role[luckyseat] = roleid # 写入玩家角色映射表
                            userlist.remove(luckyuser) # 移除预选非神玩家池里对应的玩家
                            rolegroup = headmapping[luckyrole[:2]]
                            rolespool[rolegroup].remove(luckyrole) # 移除角色池里对应角色
                            rolespool["total"].remove(luckyrole) # 移除总角色池里对应角色
                            temprolelist.remove(luckyrole) # 移除临时角色池里对应的角色
                            roleinfo = BaseRoles.objects.get(role_id=luckyrole)
                            pointlog = PointLog(
                                        room=roomid,
                                        type="2",
                                        uid=luckyuser,
                                        desc="购买指定角色卡(%s)"%(roleinfo.role_description),
                                        number=-5 # 非民5分
                                        )
                            pointloglist.append(pointlog)
                        if not userlist:
                            break

                # 然后处理非狼
                temprolelist = [*rolespool["god"],*rolespool["villagers"],*rolespool["third"]] # 临时角色池
                userlist = preselectionlist["not_wolf"] # 预选非神玩家池
                if userlist:
                    for i in range(len(temprolelist)):
                        luckyrole = random.choice(tempuserlist)
                        luckyuser = random.choice(userlist)
                        luckyseat = playerspool.get(luckyuser) # 取得座位号
                        playerspool.pop(luckyuser) # 移除选手池里对应玩家
                        if luckyseat: # 入座才算
                            player2role[luckyseat] = roleid # 写入玩家角色映射表
                            userlist.remove(luckyuser) # 移除预选非神玩家池里对应的玩家
                            rolegroup = headmapping[luckyrole[:2]]
                            rolespool[rolegroup].remove(luckyrole) # 移除角色池里对应角色
                            rolespool["total"].remove(luckyrole) # 移除总角色池里对应角色
                            temprolelist.remove(luckyrole) # 移除临时角色池里对应的角色
                            roleinfo = BaseRoles.objects.get(role_id=luckyrole)
                            pointlog = PointLog(
                                        room=roomid,
                                        type="2",
                                        uid=luckyuser,
                                        desc="购买指定角色卡(%s)"%(roleinfo.role_description),
                                        number=-5 # 非民5分
                                        )
                            pointloglist.append(pointlog)
                        if not userlist:
                            break
            # 处理剩余玩家和角色
            seatslist = []
            for k,v in playerspool.items():
                seatslist.append(v)
            roleslist = rolespool["total"]
            random.shuffle(seatslist) # 乱序
            random.shuffle(roleslist) # 乱序
            player2role = {
                **player2role,
                **dict(zip(seatslist,roleslist))
            }
            PointLog.objects.bulk_create(pointloglist)
            for k,v in player2role.items():
                k = "role" + k[6:]
                setattr(roomseats,k,v)
            roomseats.save()
            room.status = 1
            room.save()
        return Response(status=200,data=res)
