from django.http import HttpResponseRedirect
from django.views.generic import ListView,CreateView, UpdateView
from .models import RentalModel
from device.models import DeviceModel
from users.models import UsersModel
from django.urls import reverse_lazy, reverse
from .forms import RentalCreateForm, RentalEditForm, RentalReturnForm
from django.contrib import messages
import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta

#貸出管理画面
class RentalManagementView(ListView):
  template_name = "rental/rental_management.html"
  model = RentalModel
  context_object_name = "rental_list"
  
  def get_queryset(self, **kwargs):
    queryset = super().get_queryset(**kwargs)
    queryset = queryset.filter(is_deleted=False).order_by("-update_date").all()
    return queryset
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    today=datetime.date.today()
    using_list = RentalModel.objects.filter(rental_end__isnull=True).values_list("device", flat=True)
    pc_using_cnt = using_list.filter(device__device_type__contains="PC").count()
    mouse_using_cnt = using_list.filter(device__device_type__contains="マウス").count()
    other_using_cnt = using_list.filter(device__device_type__contains="その他").count()
    
    pc_cnt = DeviceModel.objects.filter(is_deleted=False, is_faulty=False, inventry_date__gt = today - relativedelta(months=6)).filter(device_type="PC").count()
    mouse_cnt = DeviceModel.objects.filter(is_deleted=False, is_faulty=False, inventry_date__gt = today - relativedelta(months=6)).filter(device_type="マウス").count()
    other_cnt = DeviceModel.objects.filter(is_deleted=False, is_faulty=False, inventry_date__gt = today - relativedelta(months=6)).filter(device_type="その他").count()
    
    context["pc_using_cnt"] = pc_using_cnt
    context["pc_cnt"] = pc_cnt
    context["mouse_using_cnt"] = mouse_using_cnt
    context["mouse_cnt"] = mouse_cnt
    context["other_using_cnt"] = other_using_cnt
    context["other_cnt"] = other_cnt
    
    now = timezone.now()
    over_scheduled = RentalModel.objects.filter(rental_scheduled__lt = now, rental_end=None).values_list("id", "user" ,"device", "rental_start", "rental_scheduled", "place").order_by("rental_scheduled")
    over_scheduled_cnt = over_scheduled.count()
    today = timezone.now()
    
    context["today"] = today
    context["over_scheduled"] = over_scheduled
    context["over_scheduled_cnt"] = over_scheduled_cnt
    
    return context
  
class RentalDetailView(UpdateView):
  template_name = "rental/rental_detail.html"
  model = RentalModel
  form_class = RentalReturnForm

  def get_success_url(self):
    return reverse("rental:rental_detail", kwargs={"pk": self.object.pk})
  
  def form_valid(self, form):
    rental = super().form_valid(form)
    messages.error(self.request, "「{}」を返却しました。".format(form.instance))
    return rental
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    today = timezone.now()
    scheduled_deadline = today + datetime.timedelta(days=1)
    return_deadline = today + relativedelta(months=3)
    context["today"] = today
    context["scheduled_deadline"] = scheduled_deadline
    context["return_deadline"] = return_deadline
    return context

def RentalDelete(request, pk):
  rental = RentalModel.objects.get(pk=pk)
  rental.is_deleted = 1
  rental.save()
  messages.error(request, "「{} {} 」の貸出履歴を削除しました。".format(rental.device, rental.user))
  return HttpResponseRedirect(reverse('rental:rental_management'))

class RentalCreateview(CreateView):
  template_name = "rental/rental_create.html"
  model = RentalModel
  success_url = reverse_lazy("rental:rental_management")
  form_class = RentalCreateForm
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      today=datetime.date.today()
      using_list = RentalModel.objects.filter(rental_end__isnull=True).values_list("device", flat=True).order_by("user_id")
      device_list = DeviceModel.objects.exclude(device_id__in=using_list).filter(is_deleted=False, is_faulty=False, inventry_date__gt=today-relativedelta(months=6), expiration_date__gt=today+timedelta(days=7)).order_by("device_id")
      context["device_list"] = device_list
      
      user_list = UsersModel.objects.filter(retirement_date__isnull=True, is_deleted=False).order_by("user_id")
      context["user_list"] = user_list
      
      return context
  
  def form_valid(self, form):
    rental= super().form_valid(form)
    messages.success(self.request, "「{}」を作成しました。".format(form.instance))
    return rental

class RentalEditView(UpdateView):
  template_name = "rental/rental_edit.html"
  model = RentalModel
  form_class = RentalEditForm
  
  def get_success_url(self):
    return reverse("rental:rental_detail", kwargs={"pk": self.object.pk})
  
  def form_valid(self, form):
    rental = super().form_valid(form)
    messages.success(self.request, "「{}」を更新しました。".format(form.instance))
    return rental
