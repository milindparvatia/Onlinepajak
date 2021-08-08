from django.contrib import admin
from app.models import Invoice, Company, Vendor

# Register your models here.
admin.site.register(Invoice)
admin.site.register(Company)
admin.site.register(Vendor)
