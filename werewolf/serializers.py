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