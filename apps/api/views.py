from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from utils import viewsets, paginatior
from apps.models import User, Server, Character, Team
from apps.api.serializers import ServerSerializer, CharacterSerializer, UserSerializer, TeamSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        return Response({"code": 0, "msg": "success", "data":{
            "access_token": data["access"],
            "token_type": "Bearer",
            "expires_in": 3600  # 根据你的配置调整
        }})


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"code": 0, "msg": "success", "data": serializer.data}, headers=headers)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    pagination_class = paginatior.PagePagination


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
