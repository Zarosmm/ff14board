from rest_framework import serializers


class UniqueRefNameModelSerializer(serializers.ModelSerializer):
    """
    自动为 DRF-YASG 设置唯一 ref_name，避免不同模块同名冲突
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls.Meta, 'ref_name'):
            # 自动生成 ref_name，例如 "模块名_类名"
            module_name = cls.__module__.split('.')[-2]  # 倒数第二级通常是 app 名
            cls.Meta.ref_name = f"{module_name}_{cls.__name__}"
        return super().__new__(cls, *args, **kwargs)