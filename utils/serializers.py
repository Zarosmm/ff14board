from rest_framework import serializers


class UniqueRefNameModelSerializer(serializers.ModelSerializer):
    """
    自动为 DRF-YASG 设置唯一 ref_name，避免不同模块同名冲突
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls.Meta, 'ref_name'):
            module_name = cls.__module__.split('.')[-2]  # 倒数第二级通常是 app 名
            cls.Meta.ref_name = f"{module_name}_{cls.__name__}"
        return super().__new__(cls, *args, **kwargs)

class ActionFieldsSerializer(UniqueRefNameModelSerializer):
    """
    动态裁剪字段，支持不同action使用不同字段
    """
    action_fields: dict[str, list | str] = {}

    action_field_serializers: dict[str, dict[str, serializers.Serializer]] = {}

    def get_fields(self):
        fields = super().get_fields()
        action = getattr(self.context.get("view"), "action", None)

        # 动态裁剪字段
        if action and action in self.action_fields:
            allowed = self.action_fields[action]
            if allowed != "__all__":
                fields = {name: field for name, field in fields.items() if name in allowed}

        # 处理 FK/M2M 字段
        if action and action in self.action_field_serializers:
            for field_name, serializer_class in self.action_field_serializers[action].items():
                if field_name in fields:
                    many = getattr(fields[field_name], "many", False)
                    fields[field_name] = serializer_class(many=many, read_only=True)

        return fields