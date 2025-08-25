from django.apps import AppConfig


class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'

    def ready(self):
        import rules
        from apps.models import User, Server, Character, Team

        # ================= User 权限 =================
        @rules.predicate
        def IsSelf(user, obj):
            return user.id == obj.id

        @rules.predicate
        def CanViewUser(user, obj):
            # 普通用户可查看所有用户，管理员绕过
            return True

        rules.add_perm("user.view_user", CanViewUser)
        rules.add_perm("user.add_user", rules.always_allow)
        rules.add_perm("user.change_user", IsSelf)
        rules.add_perm("user.delete_user", IsSelf)

        # ================= Server 权限 =================

        rules.add_perm("server.view_server", rules.always_allow)
        rules.add_perm("server.add_server", rules.always_deny)
        rules.add_perm("server.change_server", rules.always_deny)
        rules.add_perm("server.delete_server", rules.always_deny)

        # ================= Character 权限 =================
        @rules.predicate
        def IsCharacterOwner(user, obj):
            return user.id == obj.user.id

        rules.add_perm("character.view_character", rules.always_allow)
        rules.add_perm("character.add_character", rules.is_authenticated)
        rules.add_perm("character.change_character", IsCharacterOwner)
        rules.add_perm("character.delete_character", IsCharacterOwner)

        # ================= Team 权限 =================
        @rules.predicate
        def IsTeamOwner(user, obj):
            return user.id == obj.leader.user.id

        @rules.predicate
        def IsTeamMember(user, obj):
            return obj.members.filter(user=user).exists()

        rules.add_perm("team.view_team", rules.always_allow)
        rules.add_perm("team.add_team", rules.always_allow)
        rules.add_perm("team.change_team", IsTeamOwner)
        rules.add_perm("team.delete_team", IsTeamOwner)



