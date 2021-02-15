# Create your views here.

from werewolf.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from werewolf.models import *

from django.core import serializers

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