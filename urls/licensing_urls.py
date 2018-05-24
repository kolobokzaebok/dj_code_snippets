from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('company/<int:pk>', views.CompanyView.as_view(), name='company_detail'),
    path('company/add', views.AddCompany.as_view(), name='company-add'),
    path('purchaseorder/<int:pk>', views.PurchaseOrderView.as_view(), name='purchaseorder_detail'),
    path('purchaseorder/add/<company_id>', views.AddPurchaseOrder.as_view(), name="purchaseorder-add"),
    path('purchaseorder/generate/<purchaseorder_id>', views.AddLicense.as_view(), name="license-add"),
]
