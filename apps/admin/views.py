from rest_framework import generics

from utils import viewsets, paginatior
from apps.models import User, Server, Character
from apps.admin.serializers import UserSerializer, ServerSerializer, CharacterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = paginatior.PagePagination


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    pagination_class = paginatior.PagePagination


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    pagination_class = paginatior.PagePagination
