from django.db import models

class DeviceModel(models.Model):
  device_type_choices = [
    ('PC', 'PC'),
    ('マウス', 'マウス'),
    ('その他', 'その他'),
  ]

  manufacture_choices = [
    ('DELL', 'DELL'),
    ('HP', 'HP'),
    ('Lenovo', 'Lenovo'),
    ('Chrome', 'Chrome'),
    ('Apple', 'Apple'),
    ('Microsoft', 'Microsoft'),
    ('NEC', 'NEC'),
    ('FUJITSU', 'FUJITSU'),
    ('Panasonic','Panasonic'),
    ('LG Electronics', 'LG Electronics'),
    ('VAIO', 'VAIO'),
    ('dynabook', 'dynabook'),
    ('MouseComputer', 'MouseComputer'),
    ('Dospara', 'Dospara'),
    ('パソコン工房', 'パソコン工房'),
    ('ASUS', 'ASUS'),
    ('ELECOM', 'ELECOM'),
    ('BUFFALO', 'BUFFALO'),
    ('SANWA SUPPLY', 'SANWA SUPPLY'),
    ('Digio', 'Digio'),
    ('Logicool', 'Logicool'),
    ('Razer', 'Razer'),
    ('Kensington', 'Kensington'),
    ('その他', 'その他'),
  ]

  os_choices = [
    ('Windows', 'Windows'),
    ('Mac OS', 'Mac OS'),
    ('Linux', 'Linux'),
    ('Unix', 'Unix'),
    ('Chrome OS', 'Chrome OS'),
    ('その他', 'その他'),
  ]

  memory_choices = [
    ('2', '2GB'),
    ('4', '4GB'),
    ('8', '8GB'),
    ('16', '16GB'),
    ('32', '32GB'),
    ('64', '64GB'),
    ('その他', 'その他'),
  ]

  storage_choices = [
    ('128', '128GB'),
    ('256', '256GB'),
    ('512', '512GB'),
    ('1', '1TB'),
    ('2', '2TB'),
    ('その他', 'その他'),
  ]

  gpu_choices = [
    ('あり', 'あり'),
    ('なし', 'なし'),
  ]

  device_id = models.CharField(verbose_name='資産番号', unique = True, max_length=8, primary_key=True)
  manufacture = models.CharField(verbose_name='メーカー', max_length=20, choices=manufacture_choices,)
  model_name = models.CharField(verbose_name='機器名', max_length=50)
  device_type = models.CharField(verbose_name='機器タイプ', max_length=30, choices=device_type_choices,)
  os = models.CharField(verbose_name='OS', max_length=10, choices=os_choices, null=True, blank=True, default=None)
  memory = models.CharField(verbose_name='メモリ', max_length=10, choices=memory_choices, null=True, blank=True, default=None)
  storage = models.CharField(verbose_name='ストレージ', max_length=10, choices=storage_choices, null=True, blank=True, default=None)
  gpu = models.CharField(verbose_name='GPU', max_length=3, choices=gpu_choices, null=True, blank=True, default=None)
  is_faulty = models.BooleanField(verbose_name='故障', default=False, null=True)
  inventry_date = models.DateField(verbose_name='棚卸し日',)
  registration_date = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
  update_date = models.DateTimeField(verbose_name='更新日', auto_now=True)
  commencement_date = models.DateField(verbose_name='リース開始日', null=True, blank=True)
  expiration_date = models.DateField(verbose_name='リース終了日', null=True, blank=True)
  notes = models.TextField(verbose_name='備考', max_length=200, null=True, blank=True)
  is_deleted = models.BooleanField(verbose_name='削除フラグ', default=False)

  def save(self, *args, **kwargs):
    if not self.device_id:
      count_num = DeviceModel.objects.filter(device_type=self.device_type).count() + 1
      if self.device_type == 'PC':
        prefix = 'P' 
      elif self.device_type == 'マウス':
        prefix = 'M'
      else:
        prefix = 'O'
      self.device_id = f'{prefix}-{count_num:06}'
    super().save(*args, **kwargs)

  def __str__(self):
    return self.device_id