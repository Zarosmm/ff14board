import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)  # 全局唯一ID
    email = models.EmailField(unique=True)  # 确保邮箱唯一
    qq_openid = models.CharField(max_length=64, blank=True, null=True, unique=True)
    wechat_openid = models.CharField(max_length=64, blank=True, null=True, unique=True)
    avatar_url = models.URLField(blank=True, null=True)
    # 可选字段：注册来源
    oauth_provider = models.CharField(max_length=32, blank=True, null=True)  # "qq" 或 "wechat"

    def __str__(self):
        return self.username


class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)  # 全局唯一ID
    name = models.CharField(max_length=64, unique=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE, related_name="children")

    def __str__(self):
        if self.parent:
            return f"{self.parent}-{self.name}"
        return self.name


class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)  # 全局唯一ID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=64, unique=True)
    jobs = models.JSONField(default=list)

    def __str__(self):
        return f"{self.server}-{self.name}"


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)  # 全局唯一ID
    name = models.CharField(max_length=64, unique=True)
    leader = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="teamsCreated")
    members = models.ManyToManyField(Character, through='TeamCharacter', related_name="teamsJoined")
    time_slots = models.JSONField(default=list)

    def __str__(self):
        return f"{self.leader.server}-{self.name}"


class TeamCharacter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)  # 全局唯一ID
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="characterInfos")
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    job = models.CharField(max_length=64, null=False)
    gear = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.team}-{self.character.name}-{self.job}"
