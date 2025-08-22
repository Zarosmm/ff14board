from rest_framework import serializers
from utils.serializers import UniqueRefNameModelSerializer
from apps.models import Server, Character, User, Team, TeamCharacter, TeamTimeSlot


class UserRegisterSerializer(UniqueRefNameModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "qq_openid", "wechat_openid", "avatar_url", "oauth_provider"]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
        }

    def create(self, validated_data):
        # 用 create_user 确保密码哈希存储
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            qq_openid=validated_data.get("qq_openid"),
            wechat_openid=validated_data.get("wechat_openid"),
            avatar_url=validated_data.get("avatar_url"),
            oauth_provider=validated_data.get("oauth_provider"),
        )
        return user


class ServerGetSerializer(UniqueRefNameModelSerializer):
    # 递归显示子服务器
    children = serializers.SerializerMethodField()

    class Meta:
        model = Server
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        return ServerGetSerializer(obj.children.all(), many=True).data


class CharacterSerializer(UniqueRefNameModelSerializer):
    server = ServerGetSerializer(read_only=True)

    class Meta:
        model = Character
        fields = ['id', 'server', 'name', 'jobs']


class TeamSerializer(UniqueRefNameModelSerializer):

    class Meta:
        model = Team
        fields = ['id', 'name', 'leader', 'members']


class TeamCharacterSerializer(UniqueRefNameModelSerializer):
    character_name = serializers.CharField(source='character.name', read_only=True)

    class Meta:
        model = TeamCharacter
        fields = ['id', 'character', 'character_name', 'job', 'gear']


class TeamTimeSlotSerializer(UniqueRefNameModelSerializer):
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)

    class Meta:
        model = TeamTimeSlot
        fields = ['id', 'weekday', 'weekday_display', 'start_time', 'end_time']


class TeamInfoSerializer(UniqueRefNameModelSerializer):
    leader = serializers.CharField(source='leader.name', read_only=True)
    members = TeamCharacterSerializer(many=True, read_only=True, source='teamJoined')
    time_slots = TeamTimeSlotSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'leader', 'members', 'time_slots']

