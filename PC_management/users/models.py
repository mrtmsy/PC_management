from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class UsersModel(models.Model):
  gender_choice=[
    ("男性", "男性"),
    ("女性", "女性"),
    ("その他", "その他")
  ]
  position_choice=[
    ("一般", "一般"),
    ("係長", "係長"),
    ("課長","課長"),
    ("部長","部長"),
    ("取締役","取締役"),
    ("社長","社長"),
    ("その他","その他"),
  ]
  department_choice=[
    ("開発1課","開発1課"),
    ("開発2課","開発2課"),
    ("営業1課","営業1課"),
    ("営業2課","営業2課"),
    ("情報システム部","情報システム部"),
    ("その他","その他")
  ]
  authority_choice=[
    ("管理者","管理者"),
    ("利用者","利用者"),
  ]
  number_regex = RegexValidator(regex=r'^[0-9]+$')
  
  user_id = models.CharField(verbose_name="社員番号", max_length=10, unique = True, primary_key=True, validators=[number_regex],)
  name = models.CharField(verbose_name="氏名",max_length=15)
  kana_name = models.CharField(verbose_name="シメイ",max_length=15,)
  birthday = models.DateField(verbose_name="生年月日",) 
  gender = models.CharField(verbose_name="性別", max_length=5, choices=gender_choice)
  phone_number = models.CharField(verbose_name='電話番号', validators=[number_regex], max_length=15, unique=True,)
  mail = models.EmailField(verbose_name="メールアドレス", max_length=40)
  position = models.CharField(verbose_name="役職", choices=position_choice, max_length=20)
  department = models.CharField(verbose_name="部署", choices=department_choice, max_length=10)
  authority = models.CharField(verbose_name="権限", choices=authority_choice, max_length=10)
  registration_date = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
  update_date = models.DateTimeField(verbose_name='更新日', auto_now=True)
  notes = models.TextField(verbose_name='備考', max_length=200, null=True, blank=True)
  retirement_date = models.DateTimeField(verbose_name="退職日", null=True, blank=False)
  is_deleted = models.BooleanField(verbose_name='削除フラグ', default=False)
  
  def __str__(self):
    return self.user_id
  