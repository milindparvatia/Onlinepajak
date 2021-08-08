from django.urls import path, include
from .views import DataUploadView, TheVendorFilterView, TheInvoiceFilterView

urlpatterns = [
    # main index path for file upload
    path('', DataUploadView.as_view(), name='import_data'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # verification of third-parties API
    path('api/v1', TheVendorFilterView.as_view(), name='filter_third_party'),
    # scoring of commercial relationship between companies API
    path('api/v2', TheInvoiceFilterView.as_view(), name='filter_transaction'),
]