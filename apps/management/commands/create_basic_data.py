from django.core.management.base import BaseCommand
from rules import is_superuser, is_staff

from apps.models import User, Server, Team, Character
from django.contrib.auth.models import User as DjangoUser
import uuid

class Command(BaseCommand):
    help = 'Create basic data for the application'

    def handle(self, *args, **kwargs):
        # 创建管理员用户
        self.stdout.write('Creating admin user...')
        admin_user = User.objects.create_superuser(
            username='Zaros',
            email='kuzidiaolewc@outlook.com',
            password='kuzidiaole@60166',
            is_superuser=True,
            is_staff=True
        )
        self.stdout.write(f'Admin user created: {admin_user.username}')

        # 创建服务器
        self.stdout.write('Creating servers...')
        server1 = Server.objects.create(name='陆行鸟', parent=None)
        server2 = Server.objects.create(name='莫古力', parent=None)
        server3 = Server.objects.create(name='猫小胖', parent=None)
        server4 = Server.objects.create(name='豆豆柴', parent=None)
        server5 = Server.objects.create(name='白金幻象', parent=server2)
        self.stdout.write(f'Servers created: {server1.name}, {server2.name}, {server3.name}, {server4.name}, {server5.name}')



        self.stdout.write(self.style.SUCCESS('Successfully created basic data.'))

