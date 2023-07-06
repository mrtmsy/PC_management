from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import DeviceModel
from django.urls import reverse_lazy, reverse
from .forms import DeviceCreateForm, DeviceEditForm
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date

# Create your views here.

#機器管理画面
class DeviceManagementView(ListView):
  template_name = "device/device_management.html"
  model = DeviceModel

  context_object_name = "device_list"
  
  def get_queryset(self, **kwargs):
    queryset = super().get_queryset(**kwargs)
    queryset = queryset.filter(is_deleted = False).order_by("-update_date").all()
    return queryset
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    today = date.today()
    inventry_deadline = today - relativedelta(months=6)
    expirarion_deadline= today + timedelta(days=7)
    over_inventry = DeviceModel.objects.filter(is_deleted = False, inventry_date__lt = inventry_deadline).values_list("inventry_date","device_id","model_name").order_by("inventry_date")
    over_inventry_cnt = over_inventry.count()
    over_expiration = DeviceModel.objects.filter(is_deleted = False, expiration_date__lt = expirarion_deadline).values_list("expiration_date","device_id","model_name").order_by("expiration_date")
    over_expiration_cnt = over_expiration.count()
    
    context["today"] = today
    context["inventry_deadline"] = inventry_deadline
    context["over_inventry"] = over_inventry
    context["over_inventry_cnt"] = over_inventry_cnt
    context["expirarion_deadline"] = expirarion_deadline
    context["over_expiration"] = over_expiration
    context["over_expiration_cnt"] = over_expiration_cnt
    
    all_cnt = DeviceModel.objects.filter(is_deleted = False).count()
    pc_cnt = DeviceModel.objects.filter(is_deleted = False).filter(device_type="PC").count()
    mouse_cnt = DeviceModel.objects.filter(is_deleted = False).filter(device_type="マウス").count()
    other_cnt = DeviceModel.objects.filter(is_deleted = False).filter(device_type="その他").count()
    context["all_cnt"] = all_cnt
    context["pc_cnt"] = pc_cnt
    context["mouse_cnt"] = mouse_cnt
    context["other_cnt"] = other_cnt
    return context

#機器詳細画面
class DeviceDetailView(DetailView):
  template_name = "device/device_detail.html"
  model = DeviceModel
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    today = date.today()
    inventry_deadline = today - relativedelta(months=6)
    expiration_deadline = today + timedelta(days=7)
    context["today"] = today
    context["inventry_deadline"] = inventry_deadline
    context["expiration_deadline"] = expiration_deadline
    return context

#機器新規作成画面
class DeviceCreateView(CreateView):
  model = DeviceModel
  template_name = "device/device_create.html"
  success_url = reverse_lazy("device:device_management")
  context_object_name = "device_list"
  form_class = DeviceCreateForm
  
  def form_valid(self, form):
    device = super().form_valid(form)
    messages.success(self.request, "「{}」 を登録しました。".format(form.instance))
    return device

#機器編集画面
class DeviceEditView(UpdateView):
  template_name = "device/device_edit.html"
  model = DeviceModel
  form_class = DeviceEditForm
  
  def get_success_url(self):
    return reverse("device:device_detail", kwargs={"pk": self.object.pk})
  
  def form_valid(self, form):
    device = super().form_valid(form)
    messages.success(self.request, "「{}」 を更新しました。".format(form.instance))
    return device

#機器削除関数
def DeviceDelete(request, pk):
  obj = DeviceModel.objects.get(device_id=pk)
  obj.is_deleted = 1
  obj.save()
  messages.add_message(request, messages.ERROR, "「{}」 を削除しました。".format(pk))
  return HttpResponseRedirect(reverse('device:device_management'))