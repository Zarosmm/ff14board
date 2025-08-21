import datetime


def generate_file_path(instance=None, filename=""):
    today = datetime.datetime.now()
    path = today.strftime("%Y-%m-%d/%H-%M-%S/") + filename
    if instance:
        instance.path = instance._meta.model_name + "/" + filename
        return instance.path
    else:
        return path


def ManyToManyFieldSet(self, key, Model, instance, attr):
    value = self.initial_data.get(key, [])
    # 如果前端传的是字符串，按逗号分隔
    if isinstance(value, str):
        value = [v.strip() for v in value.split(",") if v.strip()]
    # 如果不是列表或字符串，直接置为空列表
    if not isinstance(value, list):
        value = []
    # 查询有效的对象
    value_list = Model.objects.filter(pk__in=value)
    # 设置 ManyToMany 关系
    getattr(instance, attr).set(value_list)
