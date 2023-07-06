from django import forms
from .models import UsersModel

#社員新規作成フォーム
class UsersCreateForm(forms.ModelForm):
  gender_choice=[
    ("男性", "男性"),
    ("女性", "女性"),
    ("その他", "その他")
  ]
  authority_choice=[
    ("管理者","管理者"),
    ("利用者","利用者"),
  ]
  gender = forms.ChoiceField(label="性別", choices=gender_choice, widget=forms.RadioSelect)
  authority = forms.ChoiceField(label="権限", choices=authority_choice, widget=forms.RadioSelect)
  
  class Meta:
    model = UsersModel
    fields = [
      "user_id",
      "name",
      "kana_name",
      "birthday",
      "gender",
      "phone_number",
      "mail",
      "position",
      "department",
      "authority",
      "notes",
    ]
    widgets = {
      "birthday": forms.DateInput(attrs={"type": "date"}),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["phone_number"].widget.attrs['placeholder'] = '09012345678'
    self.fields["mail"].widget.attrs['placeholder'] = 'example@mail.jp'

#社員編集フォーム
class UsersEditForm(forms.ModelForm):
  authority_choice=[
    ("管理者","管理者"),
    ("利用者","利用者"),
  ]
  authority = forms.ChoiceField(label="権限", choices=authority_choice, widget=forms.RadioSelect)

  class Meta:
    model = UsersModel
    fields = [
      "name",
      "kana_name",
      "phone_number",
      "mail",
      "position",
      "department",
      "authority",
      "notes",
    ]
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["phone_number"].widget.attrs['placeholder'] = '09012345678'
    self.fields["mail"].widget.attrs['placeholder'] = 'example@mail.jp'