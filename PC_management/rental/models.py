from django.db import models
from device.models import DeviceModel
from users.models import UsersModel
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your models here.

class RentalModel(models.Model):
  rental_scheduled_deadline = date.today() + relativedelta(months=3)
  
  device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, verbose_name="資産番号" )
  user = models.ForeignKey(UsersModel, on_delete=models.CASCADE, verbose_name="社員番号" )
  rental_start = models.DateTimeField(verbose_name="貸出日",)
  rental_end = models.DateTimeField(verbose_name="返却日", null=True,)
  rental_scheduled = models.DateTimeField(verbose_name="返却予定日",)
  place = models.CharField(verbose_name="設置場所", max_length=30, )
  registration_date = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
  update_date = models.DateTimeField(verbose_name='更新日', auto_now=True)
  notes = models.TextField(verbose_name='備考', max_length=200, null=True, blank=True)
  is_deleted = models.BooleanField(default=False, verbose_name="削除フラグ")
  
  def __str__(self):
    obj_name = "{} {}".format(self.device.device_id, self.user.name)
    return obj_name