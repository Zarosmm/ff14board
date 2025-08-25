from rest_framework import serializers
from utils.serializers import UniqueRefNameModelSerializer
from apps.models import Server, Character, User, Team, TeamCharacter


class UserRegisterSerializer(UniqueRefNameModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
        }

    def create(self, validated_data):
        # 用 create_user 确保密码哈希存储
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
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

    class Meta:
        model = Character
        fields = ['id', 'server', 'name', 'jobs']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        if user:
            validated_data['user'] = user
        instance = super().create(validated_data)
        return instance



class CharacterInfoSerializer(UniqueRefNameModelSerializer):
    server = ServerGetSerializer(read_only=True)

    class Meta:
        model = Character
        fields = ['id', 'server', 'name', 'jobs']


class TeamCharacterSerializer(UniqueRefNameModelSerializer):
    character = serializers.CharField(source='character.name', read_only=True)

    class Meta:
        model = TeamCharacter
        fields = ['character', 'job']


class TeamInfoSerializer(UniqueRefNameModelSerializer):
    members = TeamCharacterSerializer(many=True, read_only=True, source='teamJoined')

    class Meta:
        model = Team
        fields = ['id', 'name', 'leader', 'members', 'time_slots']
