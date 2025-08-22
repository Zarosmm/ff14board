from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from utils import viewsets, paginatior
from apps.models import User, Server, Character, Team
from apps.api.serializers import ServerGetSerializer, CharacterSerializer, UserRegisterSerializer, TeamSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerGetSerializer
    pagination_class = paginatior.PagePagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=['get'], detail=False)
    def get_server_tree(self, request):
        queryset = self.queryset.filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"code": 0, "msg": "success", "data": serializer.data})



class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    pagination_class = paginatior.PagePagination


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = paginatior.PagePagination
