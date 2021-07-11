from django.db import models
from django_currentuser.db.models import CurrentUserField


# Create your models here.
class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def inactives(self):
        return super().get_queryset().filter(is_active=False)


class BaseModel(models.Model):
    objects = BaseManager()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="最終更新日時")
    created_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_created_by",
        verbose_name="作成者", editable=False, null=True, blank=True,
    )
    last_updated_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_last_updated_by",
        verbose_name="最終更新者", editable=False, null=True, blank=True, on_update=True
    )
    is_active = models.BooleanField(default=True, verbose_name="有効")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()


class FactoryCategory(BaseModel):
    name = models.CharField("カテゴリ名", max_length=255)

    def __str__(self):
        return self.name


class Factory(BaseModel):
    name = models.CharField("工場名", max_length=255)
    detail = models.TextField("工場紹介")
    prefecture = models.CharField("都道府県", max_length=255)
    address1 = models.CharField("市町村区", max_length=255)
    address2 = models.CharField("番地", max_length=255)
    address3 = models.CharField("建物名", max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        FactoryCategory, verbose_name="カテゴリ", on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def __str__(self):
        return self.name


class AvailableProcess(BaseModel):
    name = models.CharField("対応加工名", max_length=255)

    def __str__(self):
        return self.name


class Machine(BaseModel):
    name = models.CharField("機械名", max_length=255)
    owned_by = models.ForeignKey(Factory, verbose_name="保有工場", on_delete=models.CASCADE)
    processes = models.ManyToManyField(AvailableProcess, verbose_name="対応加工", blank=True)

    def __str__(self):
        return self.name


