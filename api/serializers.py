from rest_framework import serializers, fields
from main.models import  SupplierType,Supplier,Item_category,Item_group,UOM,Branch,Company_details,Item,Purchase_Order,Stock_Receipt,BOM,StockEntry,StockRequest,BilledStock

from .models import *



class SupplierTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierType
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"

class Item_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_category
        fields = "__all__"


class Item_groupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item_group
        fields = "__all__"


class UOMSerializer(serializers.ModelSerializer):
    class Meta:
        model = UOM
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "[__all__]"

class Company_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company_details
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
class BraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class Purchase_OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase_Order
        fields = "__all__"


class Stock_ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock_Receipt
        fields = "__all__"


class BOMSerializer(serializers.ModelSerializer):
    class Meta:
        model =BOM
        fields = "__all__"

class StockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model =StockRequest
        fields = "__all__"

class StockEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model =StockEntry
        fields = "__all__"

class BilledStockSerializer(serializers.ModelSerializer):
    class Meta:
        model =BilledStock
        fields = "__all__"