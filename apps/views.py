# from rest_framework import generics
#
# from utils import viewsets, paginatior
# from apps.models import User, Server, Character
# from apps.serializers import UserSerializer, ServerSerializer, CharacterSerializer, UserRegisterSerializer
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     pagination_class = paginatior.PagePagination
#
#
# class UserRegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegisterSerializer
#
#
# class ServerViewSet(viewsets.ModelViewSet):
#     queryset = Server.objects.all()
#     serializer_class = ServerSerializer
#     pagination_class = paginatior.PagePagination
#
#
# class CharacterViewSet(viewsets.ModelViewSet):
#     queryset = Character.objects.all()
#     serializer_class = CharacterSerializer
#     pagination_class = paginatior.PagePagination
