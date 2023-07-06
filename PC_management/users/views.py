from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import UsersModel
from dateutil.relativedelta import relativedelta
from django.urls import reverse_lazy, reverse
from .forms import UsersCreateForm, UsersEditForm
from django.contrib import messages
import datetime

#社員管理画面
class UserManagementView(ListView):
  template_name = "users/users_management.html"
  model = UsersModel
  context_object_name = "users_list"
  
  def get_queryset(self, **kwargs):
    queryset = super().get_queryset(**kwargs)
    queryset = queryset.filter(is_deleted=False).order_by("-update_date").all()
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    all_cnt = UsersModel.objects.filter(is_deleted=False).count()
    enrolled_cnt = UsersModel.objects.filter(retirement_date=None, is_deleted=False).count()
    retirement_cnt = all_cnt - enrolled_cnt
    context["all_cnt"] = all_cnt
    context["enrolled_cnt"] = enrolled_cnt
    context["retirement_cnt"] = retirement_cnt
    
    return context

#社員編集画面
class UsersDetailView(DetailView):
  template_name = "users/users_detail.html"
  model = UsersModel
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = self.kwargs.get("pk")
    today = datetime.date.today()
    birthday = UsersModel.objects.values_list("birthday", flat=True).get(pk=pk)
    age = relativedelta(today, birthday)
    context["age"] = age.years
    return context

#社員退職関数
def UsersRetirement(request, pk):
  if request.method == 'POST':
    retirement_date = request.POST.get('retirement_date')
    if retirement_date:
      users = UsersModel.objects.get(pk=pk)
      users.retirement_date = retirement_date
      users.save()
      messages.error(request, "「{} {}さん」を退職にしました。".format(pk, users.name))
      return redirect('users:users_detail', pk=pk)
    else:
      return HttpResponseBadRequest("退職日を指定してください。")
  else:
    return HttpResponseBadRequest("無効なリクエストです。")

#社員削除関数
def UsersDelete(request, pk):
  users = UsersModel.objects.get(user_id=pk)
  users.is_deleted = 1
  users.save()
  messages.error(request, "「{} {}さん」をレコードから削除しました。".format(pk, users.name))
  return HttpResponseRedirect(reverse('users:users_management'))

#社員新規作成画面
class UsersCreateView(CreateView):
  model = UsersModel
  template_name = "users/users_create.html"
  success_url = reverse_lazy("users:users_management")
  form_class = UsersCreateForm
  
  def form_valid(self, form):
    users = super().form_valid(form)
    messages.success(self.request, "「{}」を登録しました".format(form.instance))
    return users

#社員編集画面
class UsersEditView(UpdateView):
  template_name = "users/users_edit.html"
  model = UsersModel
  context_object_name = "users_list"
  form_class = UsersEditForm
  
  def get_success_url(self):
    return reverse("users:users_detail", kwargs={"pk": self.object.pk})
  
  def form_valid(self, form):
    users = super().form_valid(form)
    messages.success(self.request, "「{}」を更新しました。".format(form.instance))
    return users
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = self.kwargs.get("pk")
    today = datetime.date.today()
    birthday = UsersModel.objects.values_list("birthday", flat=True).get(pk=pk)
    age = relativedelta(today, birthday)
    context["age"] = age.years
    return context