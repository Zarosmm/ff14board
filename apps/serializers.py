from rest_framework import serializers
from apps.models import Server, Character, User


class ServerSerializer(serializers.ModelSerializer):
    children = serializers.StringRelatedField(many=True, read_only=True)  # 展示子区名字

    class Meta:
        model = Server
        fields = ['id', 'name', 'parent', 'children']


class CharacterSerializer(serializers.ModelSerializer):
    server = ServerSerializer(read_only=True)

    class Meta:
        model = Character
        fields = ['id', 'server', 'name', 'jobs']


class CharacterGetSerializer(serializers.ModelSerializer):
    server = ServerSerializer(read_only=True)

    class Meta:
        model = Character
        fields = ['id', 'server', 'name', 'jobs']


class UserSerializer:
    characters = CharacterGetSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'characters', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']
