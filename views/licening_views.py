from .models import *
from django import forms
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class IndexView(generic.ListView):
    template_name = 'sales/index.html'
    context_object_name = 'company_list'

    def get_queryset(self):
        return Company.objects.all()

class CompanyView(generic.DetailView):
    model = Company
    template_name = 'sales/company_detail.html'

class PurchaseOrderView(generic.DetailView):
    model = PurchaseOrder
    template_name = 'sales/purchaseorder_detail.html'

class AddCompany(CreateView):
    model = Company
    fields = ['name', 'logo']

class AddPurchaseOrder(CreateView):
    model = PurchaseOrder
    fields = ['company', 'name', 'balance', 'license_type']

    def get_form(self):
        company = Company.objects.get(id=self.kwargs['company_id'])
        form = super(AddPurchaseOrder, self).get_form(self.form_class)
        form.fields['company'].initial = company
        form.fields['company'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super(AddPurchaseOrder, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(id=self.kwargs['company_id'])
        return context

class AddLicense(CreateView):
    model = License
    fields = ['po', 'channels']

    def get_success_url(self):
        return reverse_lazy('sales:purchaseorder_detail', args=[self.kwargs['purchaseorder_id']])

    def get_form(self):
        po = PurchaseOrder.objects.get(id=self.kwargs['purchaseorder_id'])
        form = super(AddLicense, self).get_form(self.form_class)
        form.fields['po'].initial = po
        form.fields['po'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super(AddLicense, self).get_context_data(**kwargs)
        context['purchaseorder'] = PurchaseOrder.objects.get(id=self.kwargs['purchaseorder_id'])
        return context
