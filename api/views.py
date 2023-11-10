from django.shortcuts import render
from main.models import *

# Create your views here.

from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from .models import SupplierType,Supplier,Item_category,Item_group,UOM,Branch,Company_details,Item,BranchTransfer,Purchase_Order,Stock_Receipt,BOM,StockRequest,StockEntry,BilledStock
from .serializers import (
    SupplierTypeSerializer,
    SupplierSerializer,
    Item_categorySerializer,
    Item_groupSerializer,
    UOMSerializer,
    BranchSerializer,
    Company_detailsSerializer,
    ItemSerializer,
    BraSerializer,
    Purchase_OrderSerializer,
    Stock_ReceiptSerializer,
    BOMSerializer,
    StockRequest,
    StockEntry,
    BilledStock,
)

from drf_yasg.utils import swagger_auto_schema


from .serializers import *

from django.contrib.auth.hashers import make_password


class SupplierTypeView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class =  SupplierTypeSerializer

    @swagger_auto_schema(responses={200:  SupplierTypeSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        suppliertype = SupplierType.objects.all()
        serializer =  SupplierTypeSerializer(suppliertype, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body= SupplierTypeSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers =  SupplierTypeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class SupplierView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SupplierSerializer

    @swagger_auto_schema(responses={200: SupplierSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        supplier = Supplier.objects.all()
        serializer = SupplierSerializer( supplier, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=SupplierSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = SupplierSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Item_categoryView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = Item_categorySerializer

    @swagger_auto_schema(responses={200: Item_categorySerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        item_category= Item_category.objects.all()
        serializer = Item_categorySerializer( item_category, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=Item_categorySerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = Item_categorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class UOMView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UOMSerializer

    @swagger_auto_schema(responses={200: UOMSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        uom= UOM.objects.all()
        serializer = UOMSerializer( uom, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=UOMSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = UOMSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BranchSerializer

    @swagger_auto_schema(responses={200: BranchSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        branch= Branch.objects.all()
        serializer = BranchSerializer( branch, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=BranchSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = BranchSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# class BranchView(APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = BranchSerializer

#     @swagger_auto_schema(responses={200: BranchSerializer(many=True)})
#     def  post(self, request, format=None, *args, **kwargs):
#         branch_code = kwargs.get('branch_code', None)
#         branch = Branch.objects.filter(branch_code=branch_code).first()
#         if branch is not None:
#             Branch.objects.create(
#                 branch_name=branch.name
#             )
#             return Response(status=status.HTTP_200_OK, data="Successfully ")
#         else:
#             message = {
#                 "detail": "INVALID branch code."
#             }
#         # return Response(status=status.HTTP_404_NOT_FOUND, data=message)

class Company_detailsView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = Company_detailsSerializer

    @swagger_auto_schema(responses={200: BranchSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        company_details= Company_details.objects.all()
        serializer = Company_detailsSerializer( company_details, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=Company_detailsSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = Company_detailsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Item_groupView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = Item_groupSerializer

    @swagger_auto_schema(responses={200: Item_groupSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        item_group= Item_group.objects.all()
        serializer = Item_groupSerializer( item_group, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=Item_groupSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = Item_groupSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ItemSerializer

    @swagger_auto_schema(responses={200: Item_groupSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        item= Item.objects.all()
        serializer = ItemSerializer( item, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=ItemSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = ItemSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class BraView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BraSerializer

    @swagger_auto_schema(responses={200: Item_groupSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        bra= BranchTransfer.objects.all()
        serializer = BraSerializer( bra, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=BraSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = BraSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class Purchase_OrderView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = Purchase_OrderSerializer

    @swagger_auto_schema(responses={200: Purchase_OrderSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        purchase_order= Purchase_Order.objects.all()
        serializer = Purchase_OrderSerializer( purchase_order, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=Purchase_OrderSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = Purchase_OrderSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Stock_ReceiptView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = Stock_ReceiptSerializer

    @swagger_auto_schema(responses={200: Stock_ReceiptSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        stock_receipt= Stock_Receipt.objects.all()
        serializer = Stock_ReceiptSerializer( stock_receipt, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=Stock_ReceiptSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = Stock_ReceiptSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class BOMView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BOMSerializer

    @swagger_auto_schema(responses={200: BOMSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        bom= BOM.objects.all()
        serializer = BOMSerializer( bom, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=BOMSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = BOMSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class StockRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StockRequestSerializer

    @swagger_auto_schema(responses={200: StockRequestSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        stock_request= StockRequest.objects.all()
        serializer = StockRequestSerializer( stock_request, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=StockRequestSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = StockRequestSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class StockEntryView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StockEntrySerializer

    @swagger_auto_schema(responses={200: StockEntrySerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        stock_entry= StockEntry.objects.all()
        serializer = StockEntrySerializer( stock_entry, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=StockEntrySerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = StockEntrySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class BilledStockView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BilledStockSerializer

    @swagger_auto_schema(responses={200: BilledStockSerializer(many=True)})
    def get(self, format=None, *args, **kwargs):
        billed_stock= BilledStock.objects.all()
        serializer = BilledStockSerializer( billed_stock, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=BilledStockSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializers = BilledStockSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

