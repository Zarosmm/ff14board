from rest_framework import serializers
from apps.models import User, Server, Character, Team, TeamCharacter
from utils.serializers import ActionFieldsSerializer


class UserSerializer(ActionFieldsSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "qq_openid", "wechat_openid", "avatar_url", "oauth_provider"]

    action_fields = {
        "list": ["id", "email", "username", "is_superuser"],
        "retrieve": ["id", "email", "username", "is_superuser"],
        "create": ["id", "email", "username", "password", "qq_openid", "wechat_openid", "avatar_url", "oauth_provider"],
    }


class ServerSerializer(ActionFieldsSerializer):
    class Meta:
        model = Server
        fields = ["id", "name", "parent"]

    action_fields = {
        "list": ["id", "name"],
        "retrieve": "__all__",
        "create": ["id", "name", "parent"],
    }


class CharacterSerializer(ActionFieldsSerializer):
    class Meta:
        model = Character
        fields = ["id", "user", "server", "name", "jobs"]

    action_fields = {
        "list": ["id", "name", "server"],
        "retrieve": "__all__",
        "create": ["id", "user", "server", "name", "jobs"],
    }

    # 处理 ForeignKey 和 M2M
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    server = serializers.PrimaryKeyRelatedField(queryset=Server.objects.all())


class TeamCharacterSerializer(ActionFieldsSerializer):
    class Meta:
        model = TeamCharacter
        fields = ["id", "team", "character", "job", "gear"]

    action_fields = {
        "list": ["id", "team", "character"],
        "retrieve": "__all__",
        "create": ["id", "team", "character", "job", "gear"],
    }

    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    character = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all())


class TeamSerializer(ActionFieldsSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "leader", "members", "time_slots"]

    action_fields = {
        "list": ["id", "name", "leader"],
        "retrieve": "__all__",
        "create": ["id", "name", "leader", "members", "time_slots"],
    }

    # 处理 leader (ForeignKey) 和 members (ManyToMany)
    leader = CharacterSerializer(read_only=True)
    members = TeamCharacterSerializer(many=True, read_only=True)
