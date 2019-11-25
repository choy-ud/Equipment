# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class EquipmentAttribute(models.Model):
    e_ano = models.IntegerField(db_column='E_ano', primary_key=True)  # Field name made lowercase.
    e_aname = models.CharField(db_column='E_aname', max_length=20, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'equipment_attribute'
    def __str__(self):
        return self.e_aname

class EquipmentSkill(models.Model):
    sk_no = models.IntegerField(db_column='Sk_no', primary_key=True)  # Field name made lowercase.
    sk_type = models.CharField(db_column='Sk_type', max_length=20)  # Field name made lowercase.
    sk_name = models.CharField(db_column='Sk_name', max_length=40, blank=True, null=True)  # Field name made lowercase.
    sk_describe = models.CharField(db_column='Sk_describe', max_length=400, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'equipment_skill'
    def __str__(self):
        if(self.sk_name):
            return self.sk_name
        else:
            return self.sk_describe

class EquipmentSynthesis(models.Model):
    SYN_no = models.IntegerField(db_column='SYN_no',primary_key = True, null = False)
    e_parentno = models.OneToOneField('EquipmentTotal', models.DO_NOTHING, db_column='E_parentno', related_name="E_no")  # Field name made lowercase.
    e_childno = models.OneToOneField('EquipmentTotal', models.DO_NOTHING, db_column='E_childno')  # Field name made lowercase.
    e_num = models.IntegerField(db_column='E_num')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'equipment_synthesis'


class EquipmentTAttri(models.Model):
    TA_no = models.IntegerField(db_column='TA_no',primary_key = True, null = False)
    e_no = models.OneToOneField('EquipmentTotal', models.DO_NOTHING, db_column='E_no', related_name='ae_item')  # Field name made lowercase.
    e_ano = models.OneToOneField(EquipmentAttribute, models.DO_NOTHING, db_column='E_ano', related_name='a_item')  # Field name made lowercase.
    e_adata = models.CharField(db_column='E_adata', max_length=20, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'equipment_t_attri'
        unique_together = (('e_no', 'e_ano'),)


class EquipmentTSk(models.Model):
    TSK_no = models.IntegerField(db_column='TSK_no',primary_key = True, null = False)
    e_no = models.OneToOneField('EquipmentTotal', models.DO_NOTHING, db_column='E_no', related_name='e_item')  # Field name made lowercase.
    sk_no = models.OneToOneField(EquipmentSkill, models.DO_NOTHING, db_column='Sk_no', related_name='sk_item')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'equipment_t_sk'
        unique_together = (('e_no', 'sk_no'),)


class EquipmentTotal(models.Model):
    e_no = models.IntegerField(db_column='E_no', primary_key=True)  # Field name made lowercase.
    e_name = models.CharField(db_column='E_name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    e_type = models.CharField(db_column='E_type', max_length=10, blank=True, null=True)  # Field name made lowercase.
    e_price = models.IntegerField(db_column='E_price', blank=True, null=True)  # Field name made lowercase.
    e_tprice = models.IntegerField(db_column='E_tprice', blank=True, null=True)  # Field name made lowercase.
    e_pic = models.CharField(db_column='E_pic', max_length=200, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'equipment_total'
    def __str__(self):
        return self.e_name
        
class EquipmentSet(models.Model):
    s_no = models.AutoField(db_column='S_no', primary_key=True)
    s_name = models.CharField(db_column='s_name',max_length=20,null=False)
    s_owner = models.ForeignKey(User, db_column='s_owner', related_name='s_user', on_delete=models.CASCADE)
    s_color = models.CharField(db_column='s_color',max_length=20,default='default')
    s_item1 = models.ForeignKey(EquipmentTotal, db_column='s_item1', on_delete=models.CASCADE, related_name="s_item1")
    s_item2 = models.ForeignKey(EquipmentTotal, db_column='s_item2', on_delete=models.CASCADE, related_name="s_item2")
    s_item3 = models.ForeignKey(EquipmentTotal, db_column='s_item3', on_delete=models.CASCADE, related_name="s_item3")
    s_item4 = models.ForeignKey(EquipmentTotal, db_column='s_item4', on_delete=models.CASCADE, related_name="s_item4")
    s_item5 = models.ForeignKey(EquipmentTotal, db_column='s_item5', on_delete=models.CASCADE, related_name="s_item5")
    s_item6 = models.ForeignKey(EquipmentTotal, db_column='s_item6', on_delete=models.CASCADE, related_name="s_item6")
    class Meta:
        managed = False
        db_table = 'equipment_set'