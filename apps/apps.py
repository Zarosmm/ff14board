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

        rules.add_perm("users.view_user", CanViewUser)
        rules.add_perm("users.add_user", rules.always_allow)
        rules.add_perm("users.change_user", IsSelf)
        rules.add_perm("users.delete_user", IsSelf)

        # ================= Server 权限 =================

        rules.add_perm("servers.view_server", rules.always_allow)
        rules.add_perm("servers.add_server", rules.always_deny)
        rules.add_perm("servers.change_server", rules.always_deny)
        rules.add_perm("servers.delete_server", rules.always_deny)

        # ================= Character 权限 =================
        @rules.predicate
        def IsCharacterOwner(user, obj):
            return user.id == obj.user.id

        rules.add_perm("characters.view_character", rules.always_allow)
        rules.add_perm("characters.add_character", rules.is_authenticated)
        rules.add_perm("characters.change_character", IsCharacterOwner)
        rules.add_perm("characters.delete_character", IsCharacterOwner)

        # ================= Team 权限 =================
        @rules.predicate
        def IsTeamOwner(user, obj):
            return user.id == obj.leader.user.id

        @rules.predicate
        def IsTeamMember(user, obj):
            return obj.members.filter(user=user).exists()

        rules.add_perm("teams.view_team", rules.always_allow)
        rules.add_perm("teams.add_team", rules.always_allow)
        rules.add_perm("teams.change_team", IsTeamOwner)
        rules.add_perm("teams.delete_team", IsTeamOwner)



