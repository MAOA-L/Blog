import uuid

from django.db import models


class Base(models.Model):
    """
    基础model
    """
    id = models.UUIDField(verbose_name="UUID", primary_key=True, default=uuid.uuid1)
    is_active = models.BooleanField(verbose_name="是否有效", default=True)
    gmt_created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    gmt_modified = models.DateTimeField(verbose_name="上次修改时间", auto_now=True)
    ip_addr = models.GenericIPAddressField(verbose_name="IP地址", blank=True, null=True)
