from django.contrib import admin
from factory.models import Factory, Machine, Maker, MachineType
from django.contrib.auth.models import User
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# ===========================
# Resources
# ===========================
class MachineResource(resources.ModelResource):
    class Meta:
        model = Machine
        exclude = ["created_by", "created_at", "last_updated_by", "last_updated_at"]


class FactoryResource(resources.ModelResource):
    class Meta:
        model = Factory
        exclude = ["created_by", "created_at", "last_updated_by", "last_updated_at"]


class MachineTypeResource(resources.ModelResource):
    class Meta:
        model = MachineType
        exclude = ["created_by", "created_at", "last_updated_by", "last_updated_at"]


class MakerResource(resources.ModelResource):
    class Meta:
        model = Maker
        exclude = ["created_by", "created_at", "last_updated_by", "last_updated_at"]

# ===========================
# Inlines
# ===========================
class MachineInline(admin.TabularInline):
    model = Machine
    fields = ("id", "name", "maker", "machine_type")
    max_num = 1
    can_delete = False
    readonly_fields = ("id", "name", "maker", "machine_type")


# ===========================
# ModelAdmin
# ===========================
class MakerAdmin(ImportExportModelAdmin):
    resource_class = MakerResource
    list_display = ("pk", "name", "created_at", "last_updated_at",)
    search_fields = ("name",)


class MachineTypeAdmin(ImportExportModelAdmin):
    resource_class = MachineTypeResource
    list_display = ("pk", "name", "created_at", "last_updated_at",)
    search_fields = ("name",)


class FactoryAdmin(ImportExportModelAdmin):
    resource_class = FactoryResource
    search_fields = ("name", )
    list_display = ("pk", "name", "created_at", "last_updated_at",)
    list_filter = ('prefecture', )
    inlines = (MachineInline, )


class MachineAdmin(ImportExportModelAdmin):
    resource_class = MachineResource
    autocomplete_fields = ("factory", "maker", "machine_type")
    list_display = ("pk", "name", "created_at", "last_updated_at",)
    list_filter = ("machine_type", "maker")


# ===========================
# Register
# ===========================
admin.site.register(MachineType, MachineTypeAdmin)
admin.site.register(Maker, MakerAdmin)
admin.site.register(Factory, FactoryAdmin)
admin.site.register(Machine, MachineAdmin)
