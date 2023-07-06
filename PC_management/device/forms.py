from django import forms
import datetime
from .models import DeviceModel
from dateutil.relativedelta import relativedelta

#機器新規登録フォーム
class DeviceCreateForm(forms.ModelForm):
  gpu = forms.ChoiceField(label="GPU", choices=[("あり","あり"), ("なし","なし")], widget=forms.widgets.RadioSelect,required=False)
  
  class Meta:
    model = DeviceModel
    fields = [
      "manufacture", 
      "model_name", 
      "device_type", 
      "os", 
      "memory", 
      "storage", 
      "gpu", 
      "inventry_date", 
      "commencement_date", 
      "expiration_date", 
      "notes",
    ]
    widgets = {
      "inventry_date": forms.DateInput(attrs={"type": "date"}),
      "commencement_date": forms.DateInput(attrs={"type": "date"}),
      "expiration_date": forms.DateInput(attrs={"type": "date"}),
    }
    
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['inventry_date'].initial = datetime.date.today()

  def clean(self):
    clean_data =  super().clean()
    device_type = clean_data.get("device_type")
    os = clean_data.get("os")
    memory = clean_data.get("memory")
    storage = clean_data.get("storage")
    gpu = clean_data.get("gpu")
    
    if device_type == "PC":
      if not os:
        self.add_error("os", "OSを入力してください。")
      if not memory:
        self.add_error("memory", "メモリを入力してください。")
      if not storage:
        self.add_error("storage", "ストレージを入力してください。")
      if not gpu:
        self.add_error("gpu", "GPUの有無を選択してください。")
    else:
      clean_data["os"] = ""
      clean_data["memory"] = ""
      clean_data["storage"] = ""
      clean_data["gpu"] = ""
      
      commencement_date = clean_data.get("commencement_date")
      expiration_date = clean_data.get("expiration_date")
      
      if commencement_date and expiration_date:
        if commencement_date >= expiration_date:
          self.add_error("expiration_date", "リース終了日はリース開始日より後に設定してください。")
        
    return clean_data
  
#機器編集フォーム
class DeviceEditForm(forms.ModelForm):
  class Meta:
    model = DeviceModel
    fields = [
      "os", 
      "is_faulty",
      "inventry_date", 
      "commencement_date", 
      "expiration_date", 
      "notes",
      ]
    widgets = {
      "inventry_date": forms.DateInput(attrs={"type": "date"}),
      "commencement_date": forms.DateInput(attrs={"type": "date"}),
      "expiration_date": forms.DateInput(attrs={"type": "date"}),
      }
  
    
  def clean(self):
    clean_data =  super().clean()
    device_type = self.instance.device_type
    os = clean_data.get("os")
    if device_type == "PC":
      if not os:
        self.add_error("os", "OSを入力してください。")
    
    commencement_date = clean_data.get("commencement_date")
    expiration_date = clean_data.get("expiration_date")
    
    if commencement_date and expiration_date:
      if commencement_date >= expiration_date:
        self.add_error("expiration_date", "リース終了日はリース開始日より後に設定してください。")
