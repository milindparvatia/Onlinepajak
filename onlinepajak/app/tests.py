from dateutil.parser import parse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *


class ThirdPartyTestCase(APITestCase):
    # error in testing form submit

    def test_forms(self):
        user1 = User.objects.create(username="0ccb0360-c3f3-433f-96d8-e416f13bce42")
        user2 = User.objects.create(username="485e91bd-5746-4c41-9fa2-426c65a8aed4")
        company1 = Company.objects.create(id="f4d16549-fa16-4aea-a4f8-fce904277863",
                                          company_name="PD Gunarto Rajata Tbk",
                                          npwp="45.879.488.1-037.005",
                                          email="xhidayat@cv.int",
                                          address="Gg. Dipenogoro No. 6",
                                          city="Denpasar",
                                          region="Jawa Barat",
                                          post_code=11275)
        company2 = Company.objects.create(id="adcfdc36-2967-4d22-b195-c0eb340b99fc",
                                          company_name="UD Kuswandari Tamba (Persero) Tbk",
                                          npwp="87.642.208.2-180.003",
                                          email="xriyantiraden@perum.my.id",
                                          address="Gang Siliwangi No. 26",
                                          city="Denpasar",
                                          region="Jawa Barat",
                                          post_code=85575)
        vendor1 = Vendor.objects.create(id="fc608f78-0e0c-4b56-9168-0ba556946836",
                                        vendor_name="UD Laksmiwati Megantara")
        vendor2 = Vendor.objects.create(id="544fbe6b-1092-4f92-bcf6-2dd219584879",
                                        vendor_name="CV Mayasari (Persero) Tbk")

        invoice1 = Invoice.objects.create(
            invoice_id="a052fb19-be30-4389-819b-12228c1bdb45",
            # foreign keys
            user=User.objects.get(username="485e91bd-5746-4c41-9fa2-426c65a8aed4"),
            company=Company.objects.get(id="adcfdc36-2967-4d22-b195-c0eb340b99fc"),
            vendor=Vendor.objects.get(id="544fbe6b-1092-4f92-bcf6-2dd219584879"),
            transaction_type="purchase",
            commercial_invoice_number="1.64E+12",
            status_start="REQUIRE_ACTION",
            status_tax_summary="DRAFT",
            invoice_date=parse("16/3/2021"),
            due_date=parse("17/3/2021"),
            item_name="Intuitive discrete extranet",
            unitprice=None,
            quantity=None,
            discount=None,
            gross_amount=None,
            tax_amount=None,
            total_amount=None,
            tax_period=parse("2021-03"),
            revision=None,
            reported_date=None,
            reported_status=None,
            reported_status_desc=None,
            tax_type="ppn",
            tax_document_number="91-85.28743869",
            tax_document_date=parse("16/3/21"),
            approved_date=None,
        )

        invoice1 = Invoice.objects.create(
            invoice_id="4ac647cd-f550-4a71-9fc0-4935e3fd8a6a",
            # foreign keys
            user=User.objects.get(username="0ccb0360-c3f3-433f-96d8-e416f13bce42"),
            company=Company.objects.get(id="f4d16549-fa16-4aea-a4f8-fce904277863"),
            vendor=Vendor.objects.get(id="fc608f78-0e0c-4b56-9168-0ba556946836"),
            transaction_type="purchase",
            commercial_invoice_number="1.64E+12",
            status_start="REQUIRE_ACTION",
            status_tax_summary="DRAFT",
            invoice_date=parse("12/3/2021"),
            due_date=parse("16/3/2021"),
            item_name="Intuitive discrete extranet",
            unitprice=None,
            quantity=None,
            discount=None,
            gross_amount=None,
            tax_amount=None,
            total_amount=None,
            tax_period=parse("2021-03"),
            revision=None,
            reported_date=None,
            reported_status=None,
            reported_status_desc=None,
            tax_type="ppn",
            tax_document_number="76-00.65880146",
            tax_document_date=parse("12/3/2021"),
            approved_date=None,
        )
        self.assertEqual(user1.username, User.get_username(user1))

    def invoice_testing(self):
        response = self.client.get('/v2?company_name=Perum Uyainah (Persero) Tbk&vendor_name=PD Hasanah')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_transactions"], "1")

    def third_party_company_testing(self):

        response = self.client.get('/v1?vendor_name=UD Laksmiwati Megantara')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["third_party_company_exist"], True)
