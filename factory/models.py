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
    # CHOICES
    CHOICES_LAYER = ((1, "1. 大分類"), (2, "2. 中分類"), (3, "3. 小分類"),)
    # FIELDS
    name = models.CharField("カテゴリ名", max_length=255)
    layer = models.IntegerField("階層", choices=CHOICES_LAYER, default=1)
    parent_category = models.ForeignKey(
        "self", blank=True, null=True,
        verbose_name="親カテゴリ", related_name="child_categories", on_delete=models.CASCADE
    )

    def __str__(self):
        if self.layer == 1:
            return self.name
        elif self.layer == 2:
            return "{} / {}".format(self.parent_category.name, self.name)
        elif self.layer == 3:
            return "{} / {} / {}".format(
                self.parent_category.parent_category.name, self.parent_category.name, self.name)

    def save(self, *args, **kwargs):
        if self.layer == 1 and self.parent_category:
            raise Exception('Category of Layer1 should not have parent_category')
        elif self.layer == 2 and (self.parent_category is None or self.parent_category.layer != 1):
            raise Exception('Category of Layer2 should have parent_category of Layer1')
        elif self.layer == 3 and (self.parent_category is None or self.parent_category.layer != 2):
            raise Exception('Category of Layer3 should have parent_category of Layer2')
        return super(FactoryCategory, self).save()

    @property
    def layer1(self):
        if self.layer == 1:
            return self
        elif self.layer == 2:
            return self.parent_category
        elif self.layer == 3:
            return self.parent_category.parent_category

    @property
    def layer2(self):
        if self.layer == 1:
            return None
        elif self.layer == 2:
            return self
        elif self.layer == 3:
            return self.parent_category

    @property
    def layer3(self):
        if self.layer == 3:
            return self
        else:
            return None

    @property
    def num_linked_factories(self):
        if self.layer == 3:
            return Factory.objects.filter(is_active=True, category=self).count()
        elif self.layer == 2:
            return Factory.objects.filter(is_active=True, category__in=self.child_categories.all()).count()
        elif self.layer == 1:
            num = 0
            for gchild in self.child_categories.all():
                num += gchild.num_linked_factories
            return num


class Factory(BaseModel):
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
    name = models.CharField("工場名", max_length=255)
    detail = models.TextField("工場紹介")
    prefecture = models.CharField("都道府県", max_length=255, choices=CHOICES_PREFECTURE)
    address1 = models.CharField("市町村区", max_length=255)
    address2 = models.CharField("番地", max_length=255)
    address3 = models.CharField("建物名", max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        FactoryCategory, verbose_name="カテゴリ", on_delete=models.DO_NOTHING, blank=True, null=True,
        limit_choices_to={"layer": 3, "is_active": True},
    )

    def __str__(self):
        return self.name


class AvailableProcess(BaseModel):
    name = models.CharField("対応加工名", max_length=255)

    def __str__(self):
        return self.name


class Material(BaseModel):
    name = models.CharField("材質名", max_length=255)

    def __str__(self):
        return self.name


class Machine(BaseModel):
    CHOICES_ACCURACY = (
        ("10分台", "10分台"),
        ("100分台", "100分台"),
        ("1000分台", "1000分台"),
    )
    name = models.CharField("機械名", max_length=255)
    owned_by = models.ForeignKey(
        Factory, verbose_name="保有工場", on_delete=models.CASCADE, limit_choices_to={"is_active": True},)
    processes = models.ManyToManyField(
        AvailableProcess, blank=True, verbose_name="対応加工", limit_choices_to={"is_active": True},)
    available_size_height = models.IntegerField("対応加工な製品サイズ（縦）", null=True, blank=True)
    available_size_width = models.IntegerField("対応加工な製品サイズ（横）", null=True, blank=True)
    available_size_diagon = models.IntegerField("対応加工な製品サイズ（斜め）", null=True, blank=True)
    materials = models.ManyToManyField(
        Material, blank=True, verbose_name="材質", limit_choices_to={"is_active": True},)
    accuracy = models.CharField("加工精度（上限）", max_length=255, choices=CHOICES_ACCURACY, blank=True, null=True)
    detail = models.TextField("備考・詳細", blank=True, null=True)
    processes_other = models.CharField("対応可能（その他）", max_length=255, blank=True, null=True)

#     機械名 自由記述
#     対応加工 MAリスト
#     加工可能な製品サイズ
#     縦 自由記述(数値)
#     横 自由記述(数値)
#     斜め 自由記述(数値)
#     材質 MAリスト
#     加工精度（上限）        SAリスト
#     最短製作日数  自由記述(数値)
#     備考・詳細 自由記述（text）
#     対応加工（その他）

    def __str__(self):
        return self.name


