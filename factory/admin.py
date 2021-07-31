from django.contrib import admin
from factory.models import Factory, FactoryCategory, Machine, AvailableProcess, Material
from django.contrib.auth.models import User
# Register your models here.


class MachineInline(admin.TabularInline):
    model = Machine
    fields = ("id", "name", "processes", "materials")
    max_num = 1
    can_delete = False
    readonly_fields = ("id", "name", "processes", "materials")


class FactoryCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_display = ("pk", "layer", "name", "created_at", "last_updated_at", )
    readonly_fields = ("layer1", "layer2", "layer3")
    ordering = ("layer", )
    list_filter = ("layer", )


class MachineAdmin(admin.ModelAdmin):
    autocomplete_fields = ("owned_by", "processes")
    list_display = ("pk", "name", "created_at", "last_updated_at",)


class FactoryAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    autocomplete_fields = ("category",)
    list_display = ("pk", "name", "_layer1", "_layer2", "_layer3", "created_at", "last_updated_at",)
    list_filter = (
        "machine",
        "machine__processes",
        "machine__materials",
        "category",
        # "category__parent_category",
        # "category__parent_category__parent_category",
    )
    inlines = (MachineInline, )

    def _layer1(self, obj):
        return obj.category.layer1

    def _layer2(self, obj):
        return obj.category.layer2

    def _layer3(self, obj):
        return obj.category.layer3

    _layer1.short_description = "大分類"
    _layer2.short_description = "中分類"
    _layer3.short_description = "小分類"


class AvailableProcessAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("pk", "name", "created_at", "last_updated_at",)


admin.site.register(Factory, FactoryAdmin)
admin.site.register(FactoryCategory, FactoryCategoryAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(AvailableProcess, AvailableProcessAdmin)
admin.site.register(Material)
