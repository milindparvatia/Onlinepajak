from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Company model
class Company(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    company_name = models.CharField(max_length=42)
    npwp = models.CharField(max_length=20)
    email = models.CharField(max_length=32)
    address = models.CharField(max_length=33)
    city = models.CharField(max_length=33)
    region = models.CharField(max_length=19)
    post_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.company_name


# Vendor model
class Vendor(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    vendor_name = models.CharField(max_length=42)

    def __str__(self):
        return self.vendor_name


# Invoice model
class Invoice(models.Model):
    invoice_id = models.CharField(max_length=36)

    # foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, )

    transaction_type = models.CharField(max_length=8)
    commercial_invoice_number = models.CharField(max_length=13)
    status_start = models.CharField(max_length=14)
    status_tax_summary = models.CharField(max_length=11, null=True)
    invoice_date = models.DateField(null=True, blank=True, default='')
    due_date = models.DateField(null=True, blank=True, default='')
    item_name = models.CharField(max_length=61)

    # Float values
    unitprice = models.FloatField(null=True, blank=True, default='')
    quantity = models.FloatField(null=True, blank=True, default='')
    discount = models.FloatField(null=True, blank=True, default='')
    gross_amount = models.FloatField(null=True, blank=True, default='')
    tax_amount = models.FloatField(null=True, blank=True, default='')
    total_amount = models.FloatField(null=True, blank=True, default='')

    tax_period = models.CharField(max_length=7, null=True, blank=True, default='')
    revision = models.IntegerField(null=True, blank=True, default='')
    reported_date = models.DateTimeField(null=True, blank=True, default='')
    reported_status = models.CharField(max_length=4, null=True, blank=True, default='')
    reported_status_desc = models.CharField(max_length=12, null=True, blank=True, default='')
    tax_type = models.CharField(max_length=8, null=True, blank=True, default='')
    tax_document_number = models.CharField(max_length=14, default='')
    tax_document_date = models.DateField(null=True, blank=True, default='')
    approved_date = models.DateTimeField(null=True, blank=True, default='')

    def __str__(self):
        return self.invoice_id
