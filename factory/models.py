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


class Factory(BaseModel):
    class Meta:
        verbose_name = "工場"
        verbose_name_plural = "工場"

    def __str__(self):
        return self.name

    # CHOICES
    CHOICES_PREFECTURE = (
        (k, k) for k in (
            "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
            "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
            "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
            "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
            "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
            "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
            "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県", "-"
        )
    )

    # fields
    name = models.CharField("名前", max_length=255)
    detail = models.TextField("工場詳細", blank=True, null=True)
    prefecture = models.CharField("都道府県", max_length=255, choices=CHOICES_PREFECTURE)
    address1 = models.CharField("市町村区", max_length=255)
    address2 = models.CharField("番地", max_length=255)
    address3 = models.CharField("建物名", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Maker(BaseModel):
    class Meta:
        verbose_name = "メーカー"
        verbose_name_plural = "メーカー"

    def __str__(self):
        return self.name

    name = models.CharField("名前", max_length=255, unique=True)


class MachineType(BaseModel):
    class Meta:
        verbose_name = "機械種別"
        verbose_name_plural = "機械種別"
        
    def __str__(self):
        return self.name

    name = models.CharField("名前", max_length=255, unique=True)


class Machine(BaseModel):
    class Meta:
        verbose_name = "機械"
        verbose_name_plural = "機械"

    def __str__(self):
        return self.name

    name = models.CharField("名前", max_length=255)
    maker = models.ForeignKey(
        Maker, verbose_name='メーカー', on_delete=models.CASCADE, limit_choices_to={"is_active": True},)
    machine_type = models.ForeignKey(
        MachineType, verbose_name='機械種別', on_delete=models.CASCADE, limit_choices_to={"is_active": True},)
    factory = models.ForeignKey(
        Factory, verbose_name="保有工場", on_delete=models.CASCADE, limit_choices_to={"is_active": True},)
    detail = models.TextField("備考・詳細", blank=True, null=True)

