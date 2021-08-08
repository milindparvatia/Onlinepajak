import csv
import io

from dateutil.parser import parse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, Invoice, Vendor


# importing data to DATABASE
class DataUploadView(View):

    def get(self, request):
        template_name = 'import_data.html'
        return render(request, template_name)

    def post(self, request):
        param_file = io.TextIOWrapper(request.FILES['data'].file)
        data = csv.DictReader(param_file)
        list_of_dict = list(data)

        vendor_objs = [
            Vendor(
                id=row['vendor_id'],
                vendor_name=row['vendor_name'],
            )
            for row in list_of_dict
        ]

        Company_objs = [
            Company(
                id=row['company_id'],
                company_name=row['company_name'],
                npwp=row['npwp'],
                email=row['email'],
                address=row['address'],
                city=row['city'],
                region=row['region'],
                post_code=row['post_code'],
            )
            for row in list_of_dict
        ]

        password = make_password("admin"),

        user_objs = [
            User(
                username=row['user_id'],
                email='admin@email.com',
                password=password,
                is_active=True,
            )
            for row in list_of_dict
        ]

        try:
            create_company = Company.objects.bulk_create(
                objs=Company_objs, ignore_conflicts=True)
            print("create_company")
            create_user = User.objects.bulk_create(
                objs=user_objs, ignore_conflicts=True)
            print("create_user")
            create_vendor = Vendor.objects.bulk_create(
                objs=vendor_objs, ignore_conflicts=True)
            print("create_vendor")

            invoice_objs = [
                Invoice(
                    invoice_id=row['invoice_id'],
                    user=User.objects.get(username=row['user_id']),
                    company=Company.objects.get(id=row['company_id']),
                    vendor=Vendor.objects.get(id=row['vendor_id']),
                    transaction_type=row['transaction_type'],
                    commercial_invoice_number=row['commercial_invoice_number'],
                    status_start=row['status_start'],
                    status_tax_summary=row['status_tax_summary'],
                    invoice_date=parse(row['invoice_date']),
                    due_date=parse(row['due_date']),
                    item_name=row['item_name'],
                    unitprice=row['unitprice'] if row['unitprice'] else None,
                    quantity=row['quantity'] if row['quantity'] else None,
                    discount=row['discount'] if row['discount'] else None,
                    gross_amount=row['gross_amount'] if row['gross_amount'] else None,
                    tax_amount=row['tax_amount'] if row['tax_amount'] else None,
                    total_amount=row['total_amount'] if row['total_amount'] else None,
                    tax_period=row['tax_period'],
                    revision=row['revision'] if row['revision'] else None,
                    reported_date=parse(
                        row['reported_date']) if row['reported_date'] else None,
                    reported_status=row['reported_status'],
                    reported_status_desc=row['reported_status_desc'],
                    tax_type=row['tax_type'],
                    tax_document_number=row['tax_document_number'],
                    tax_document_date=parse(
                        row['tax_document_date']) if row['tax_document_date'] else None,
                    approved_date=parse(
                        row['approved_date']) if row['approved_date'] else None,
                ) for row in list_of_dict
            ]

            try:

                create_invoice = Invoice.objects.bulk_create(objs=invoice_objs)
                print("create_invoice")

                returnmsg = {"status_code": 200}
                print('imported successfully')
            except Exception as e:
                print('Error While Importing Data: ', e)
                returnmsg = {"status_code": 500}

            returnmsg = {"status_code": 200}
            print('imported successfully')
        except Exception as e:
            print('Error While Importing Data: ', e)
            returnmsg = {"status_code": 500}

        return JsonResponse(returnmsg)


# 1) verification of third-parties:
class TheVendorFilterView(APIView):
    queryset = Vendor.objects.all()

    def get(self, format=None):
        queryset = self.queryset

        try:
            keyword = self.request.query_params.get('vendor_name', '')
            if keyword:
                ### Main Queryset filter
                query_set = queryset.filter(vendor_name__iexact=keyword)

                if not query_set:
                    print('Vendor_name is not in dataset ')
                    return Response({
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "error_msg": "third-party company name is not in dataset"
                    })
            else:
                print('Vendor_name not provided: ')
                return Response({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "error_msg": "third-party company name is not provided!!"
                })
        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error_msg": "Error While fetching Data from vendor filter"
            })
        return Response({
            "status_code": status.HTTP_200_OK,
            "third_party_company_exist": True if query_set else False
        })


# 2)  scoring of commercial relationship between companies:
class TheInvoiceFilterView(APIView):
    queryset = Invoice.objects.all()

    def get(self, format=None):
        queryset = self.queryset

        try:
            cname_1 = self.request.query_params.get('company_name', '')
            cname_2 = self.request.query_params.get('vendor_name', '')

            if cname_1 and cname_2:
                ### Main Queryset filter
                query_set = queryset.filter(company_id__company_name__iexact=cname_1).filter(
                    vendor_id__vendor_name__iexact=cname_2)

                if not query_set:
                    print('Vendor_name is not in dataset ')
                    return Response({
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "error_msg": "No transaction found between these companies in dataset"
                    })
            else:
                if not cname_1:
                    return Response({
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "error_msg": "first company name is not in dataset"
                    })

                if not cname_2:
                    return Response({
                        "status_code": status.HTTP_404_NOT_FOUND,
                        "error_msg": "second company name is not in dataset"
                    })
        except Exception as e:
            return Response({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error_msg": "Error While fetching Data from vendor filter"
            })
        return Response({
            "status_code": status.HTTP_200_OK,
            "total_transactions": query_set.count()
        })
