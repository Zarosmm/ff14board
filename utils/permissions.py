from rest_framework.permissions import BasePermission, SAFE_METHODS
import rules


class RulesPermission(BasePermission):
    """
    通用 DRF 权限类，结合 django-rules。
    """

    def has_permission(self, request, view):
        return True
        # 列表或创建等全局操作
        if request.method in SAFE_METHODS:
            return True  # GET/HEAD/OPTIONS 默认允许
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return True
        # 映射 HTTP 方法到操作类型
        method_map = {
            'GET': 'view',
            'HEAD': 'view',
            'OPTIONS': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
        }
        action = method_map.get(request.method)
        if not action:
            return False

        model_cls = obj.__class__
        perm_name = f"{model_cls._meta.model_name}.{action}_{model_cls._meta.model_name}"

        return rules.has_perm(perm_name, request.user, obj)
