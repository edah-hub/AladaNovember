from django.urls import path
from . import views

    
urlpatterns = [
    path('supplier_type', views.SupplierTypeView.as_view(),name='suppliertype_api'),
    path('supplier', views.SupplierView.as_view(),name='supplier_api'),
    path('item_category', views.Item_categoryView.as_view(),name='item_category_api'),
    path('item_group', views.Item_groupView.as_view(),name='item_group_api'),
    path('uom', views.UOMView.as_view(),name='uom_api'),
    # path('branch', views.BranchView.as_view(),name='branch_api'),
    path("branch/<str:branch_code>", views.BranchView.as_view(), name="branch_api"),
    
    path('comapny_details', views.Company_detailsView.as_view(),name='company_details_api'),
    path('item', views.ItemView.as_view(),name='item_api'),
    path('branchtransfer', views.BraView.as_view(),name='branchtransfer'),
    path('purchase_order', views.Purchase_OrderView.as_view(),name='purchase_order_api'),
    path('stock_receipt', views.Stock_ReceiptView.as_view(),name='stock_receipt_api'),
    path('bom', views.BOMView.as_view(),name='bom_api'),
    path('stock_request', views.StockRequestView.as_view(),name='stock_request_api'),
    path('stock_entry', views.StockEntryView.as_view(),name='stock_entry_api'),
    path('billed_stock', views.BilledStockView.as_view(),name='billed_stock_api'),
    
    
]