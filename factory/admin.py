from django.contrib import admin
from factory.models import Factory, FactoryCategory, Machine, AvailableProcess
from django.contrib.auth.models import User
# Register your models here.


class MachineInline(admin.TabularInline):
    model = Machine
    fields = ("id", "name", "processes")
    max_num = 1
    can_delete = False
    readonly_fields = ("id", "name", "processes")


class FactoryCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    list_display = ("pk", "name", "created_at", "last_updated_at", )


class MachineAdmin(admin.ModelAdmin):
    autocomplete_fields = ("owned_by", "processes")
    list_display = ("pk", "name", "created_at", "last_updated_at",)


class FactoryAdmin(admin.ModelAdmin):
    search_fields = ("name", )
    autocomplete_fields = ("category",)
    list_display = ("pk", "name", "created_at", "last_updated_at",)
    list_filter = ("machine", "machine__processes")
    inlines = (MachineInline, )


class AvailableProcessAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("pk", "name", "created_at", "last_updated_at",)


admin.site.register(Factory, FactoryAdmin)
admin.site.register(FactoryCategory, FactoryCategoryAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(AvailableProcess, AvailableProcessAdmin)