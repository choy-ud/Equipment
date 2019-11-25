from django.contrib import admin
from imitator.models import *
# Register your models here.

class EquipmentSkillAdmin(admin.ModelAdmin):
    list_display=('sk_no','sk_name','sk_type','sk_describe')

admin.site.register(EquipmentSkill,EquipmentSkillAdmin)


class EquipmentTotalAdmin(admin.ModelAdmin):
    list_display=('e_no','e_name','e_price','e_tprice')

admin.site.register(EquipmentTotal,EquipmentTotalAdmin)

class EquipmentTAttriAdmin(admin.ModelAdmin):
    list_display=('TA_no','e_no','e_ano','e_adata')

admin.site.register(EquipmentTAttri,EquipmentTAttriAdmin)

class EquipmentTSkAdmin(admin.ModelAdmin):
    list_display=('TSK_no','e_no','sk_no')

admin.site.register(EquipmentTSk,EquipmentTSkAdmin)

class EquipmentSynthesisAdmin(admin.ModelAdmin):
    list_display=('SYN_no','e_parentno','e_childno','e_num')

admin.site.register(EquipmentSynthesis,EquipmentSynthesisAdmin)