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