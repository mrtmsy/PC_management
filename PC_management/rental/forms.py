from django import forms
from .models import RentalModel
from device.models import DeviceModel
from users.models import UsersModel
from dateutil.relativedelta import relativedelta

#貸出新規登録フォーム
class RentalCreateForm(forms.ModelForm):
  using_list = RentalModel.objects.filter(rental_end__isnull=True).values_list("device", flat=True)
  device_list = DeviceModel.objects.exclude(device_id__in=using_list).filter(is_deleted=False)
  device = forms.ModelChoiceField(queryset=device_list, label="資産番号", widget=forms.TextInput(attrs={"readonly": "readonly"}))
  user = forms.ModelChoiceField(queryset=UsersModel.objects.filter(retirement_date__isnull=True), label="社員番号", widget=forms.TextInput(attrs={"readonly": "readonly"}))
  
  class Meta:
    model = RentalModel
    fields = [
      "device",
      "user",
      "rental_start",
      "rental_scheduled",
      "place",
      "notes",
    ]
    widgets = {
      "rental_start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
      "rental_scheduled": forms.DateTimeInput(attrs={"type": "datetime-local"}),
    }
  
  def clean(self):
    clean_data =  super().clean()
    rental_start = clean_data.get("rental_start")
    rental_scheduled = clean_data.get("rental_scheduled")
    rental_deadline = rental_start + relativedelta(months=3)
    
    if rental_scheduled > rental_deadline:
      self.add_error("rental_scheduled", "貸出は最大3ヶ月までです。")
    
    if rental_start and rental_scheduled:
      if rental_start >= rental_scheduled:
        self.add_error("rental_scheduled", "返却予定日は貸出日より後に設定してください。")

#貸出編集フォーム
class RentalEditForm(forms.ModelForm):
  class Meta:
    model = RentalModel
    fields = [
      "rental_scheduled",
      "place",
      "notes",
    ]
    widgets = {
      "rental_start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
      "rental_scheduled": forms.DateTimeInput(attrs={"type": "datetime-local"}),
    }
  
  def clean(self):
    clean_data =  super().clean()
    rental_start = self.instance.rental_start
    rental_scheduled = clean_data.get("rental_scheduled")
    rental_deadline = rental_start + relativedelta(months=3)
    
    if rental_scheduled > rental_deadline:
      self.add_error("rental_scheduled", "貸出は最大3ヶ月までです。")
    
    if rental_start and rental_scheduled:
      if rental_start >= rental_scheduled:
        self.add_error("rental_scheduled", "返却予定日は貸出日より後に設定してください。")
    
#返却フォーム
class RentalReturnForm(forms.ModelForm):
  class Meta:
    model = RentalModel
    fields = [
      "rental_end"
    ]

    widgets = {
      "rental_end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
    }
    
  def clean(self):
    clean_data =  super().clean()
    rental_start = self.instance.rental_start
    print(rental_start)
    rental_end = clean_data.get("rental_end")
    print(rental_end)
    if rental_end <= rental_start:
      self.add_error("rental_end", "返却日は貸出日より後に設定してください。")