from urllib import request, response
from django.contrib import messages
from .utils import *
import requests
import pandas as pd
import json, random, string, re
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from decimal import Decimal
from main.EmailBackEnd import EmailBackEnd
import uuid
import pandas as pd
from django.core.paginator import Paginator


from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django_daraja.mpesa.core import MpesaClient
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django_daraja.mpesa import utils
from django.views.generic import View
from decouple import config
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# from .forms import UserRegistrationForm
from django.contrib import messages
from .connecting_transaction_module import all_transaction_process, transaction_login
from .get_service_fields import get_service_fields, get_service_metadata
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models import Q
from .check_user_role import *

BASE_URL = "http://bharathbrandsdotin.pythonanywhere.com/api-alada/"


# home view
def home(request):
    request.session["mode"] = "client"
    return render(request, "home.html")


def dashboard(request):
    if request.user.is_authenticated:
        check_function_name = (
            "dashboard"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)
        supplier_count = Supplier.objects.count()
        product_count = Item.objects.count()
        category_count = Item_category.objects.count()
        user_count = User.objects.count()

        if check_function_name in access_functions or is_superuser:
            context = {
                "supplier_count": supplier_count,
                "product_count": product_count,
                "category_count": category_count,
                "user_count": user_count,
            }
            return render(request, "dashboard.html", context)
        else:
            return redirect("error_page")  # Redirect to error page if no permission
    else:
        return redirect("login_views")  # Redirect to login page if not authenticated


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Use the correct field names for password
            user.set_password(form.cleaned_data["password1"])  # Use password1
            user.save()

            messages.success(
                request, f"Your account has been created. You can log in now!"
            )
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)


# Add supplier type.


def add_supplier_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_supplier_type"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                form = SupplierTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect(
                        "show_supplier_type"
                    )  # Redirect after successful submission
            else:
                form = SupplierTypeForm()

            context = {"form": form}
            return render(request, "add_supplier_type.html", context)
        else:
            return redirect("error_page")  # Redirect to error page if no permission
    else:
        return redirect("login_views")  # Redirect to login page if not authenticated


# To show supplier type
def show_supplier_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "show_supplier_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            suppliers = Supplier.objects.all()
            return render(request, "view_supplier_type.html", {"suppliers": suppliers})
        else:
            return redirect(
                "error_page"
            )  # Redirect to an error page for unauthorized access
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# To edit supplier type
def edit_supplier_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "edit_supplier_type"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "edit_supplier.html")
        else:
            return redirect("error_page")  # Redirect to error page if no permission
    else:
        return redirect("login_views")  # Redirect to login page if not authenticated


# add_supplier
# res1 = request.session['user_allowed_func']
def add_supplier(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_supplier"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = SupplierForm()

            if request.method == "POST":
                form = SupplierForm(request.POST)

                if form.is_valid():
                    form.save()
                    return redirect("views_suppliers")
                else:
                    messages.info(request, message="Could not save supplier")
                    return redirect("add_supplier")

            return render(request, "add_supplier.html", {"form": form})
        else:
            return redirect("error_page")  # Redirect to error page if no permission
    else:
        return redirect("login_views")  # Redirect to login page if not authenticated


# view_supplier
# res1 = my_requests.session['user_allowed_func']
def views_suppliers(request):
    if request.user.is_authenticated:
        check_function_name = (
            "views_suppliers"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            suppliers = Supplier.objects.all()
            context = {"suppliers": suppliers}
            return render(request, "view_suppliers.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


from .models import Item


def add_product(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_product"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                form = ItemForm(request.POST)
                item_code = Item.generate_itemcode()
                if form.is_valid():
                    new_item = form.save(commit=False)
                    new_item.item_code = item_code
                    new_item.save()
                    return redirect("show_product")
            else:
                form = ItemForm()
            return render(request, "add_product.html", {"form": form})
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


# To show product


def show_product(request):
    if request.user.is_authenticated:
        check_function_name = (
            "show_product"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            search_query = request.GET.get("search_query")
            items = Item.objects.all()

            if search_query:
                items = items.filter(
                    Q(item_name__icontains=search_query)
                    | Q(item_code__icontains=search_query)
                    | Q(item_category__category_name__icontains=search_query)
                )

            context = {"items": items}
            return render(request, "show_product.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")
    
# To edit product
def edit_product(request, id):
    if request.user.is_authenticated:
        check_function_name = (
            "edit_product"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            item = get_object_or_404(Item, id=id)

            if request.method == "POST":
                form = ItemForm(request.POST, instance=item)
                if form.is_valid():
                    form.save()
                    return redirect("show_product")
            else:
                form = ItemForm(instance=item)

            return render(
                request,
                "edit_product.html",
                {
                    "form": form,
                },
            )
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")



# item bulk upload
def item_bulk_upload(request):
    if request.method == "POST":
        form = ItemBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]

            # Check the file type (CSV or Excel) and read data accordingly
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file)

            # Loop through the DataFrame and create Item objects
            for index, row in df.iterrows():
                # Get or create the Item_category instance based on the 'Item Category' from the file
                category_name = row["Category"]
                item_category, _ = Item_category.objects.get_or_create(
                    category_name=category_name
                )

                # Get or create a default item group instance
                # default_group_name = 'Default Item Group'
                # default_item_group, _ = Item_group.objects.get_or_create(group_name=default_group_name)

                # Get or create the Item_group instance based on the 'Item Group' from the file
                group_name = row["Group"]
                item_group, _ = Item_group.objects.get_or_create(group_name=group_name)

                # Get or create the UOM instance based on the 'Item UOM' from the file
                UOM_name = row["UoM"]
                item_UOM, _ = UOM.objects.get_or_create(UOM_name=UOM_name)

                Item.objects.create(
                    item_name=row["ProductName"],
                    item_code=row["ProductCode"],
                    item_category=item_category,
                    item_group=item_group,
                    item_UOM=item_UOM,
                    # receveive_quantity=row['Receive Quantity'],
                    # receive_by=row['Receive By'],
                    # issue_quantity=row['Issue Quantity'],
                    # issue_by=row['Issue By'],
                    # issue_to=row['Issue To'],
                    # created_by=row['Created By'],
                    # reorder_level=row['Reorder Level'],
                    # Add other fields as needed
                )

            # Redirect to a success page or display a success message
            return redirect("success")

    else:
        form = ItemBulkUploadForm()

    return render(request, "bulk_upload.html", {"form": form})


# Add stocks balance


def add_stocks_balance(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_stocks_balance"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                form = StocksBalanceForm(request.POST)
                if form.is_valid():
                    item = form.cleaned_data["item"]
                    branch = form.cleaned_data["branch"]
                    item_quantity = form.cleaned_data["item_quantity"]
                    branch_item, created = stockbalanceCreate.objects.get_or_create(
                        item=item, branch=branch
                    )
                    branch_item.item_quantity += item_quantity
                    branch_item.save()
                    return redirect("/stocks_balance")
            else:
                form = StocksBalanceForm()
            return render(request, "add_stocks_balance.html", {"form": form})
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


def sort_by_date(items, date_attr, reverse=False):
    return sorted(items, key=lambda x: getattr(x, date_attr), reverse=reverse)


from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Branch, Item, stockbalanceCreate


def stocks_balance(request):
    if request.user.is_authenticated:
        check_function_name = "stocks_balance"
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            branches = Branch.objects.all()
            items = Item.objects.all()
            stock_balance_data = []
            search_query = request.GET.get("search_query")
            sort_by = request.GET.get("sort_by", "created_date")
            sort_order = request.GET.get("sort_order", "asc")

            if search_query:
                items = items.filter(
                    Q(item_name__icontains=search_query)
                    | Q(item_code__icontains=search_query)
                    | Q(item_category__category_name__icontains=search_query)
                )

            if sort_by == "item_name":
                items = items.order_by(
                    "item_name" if sort_order == "asc" else "-item_name"
                )
            elif sort_by == "item_code":
                items = items.order_by(
                    "item_code" if sort_order == "asc" else "-item_code"
                )

            # Create a Paginator instance
            paginator = Paginator(items, 10)  # Change 10 to the desired items per page

            # Get the current page number from the request's GET parameters
            page_number = request.GET.get("page")

            # Get the Page object for the current page
            items_page = paginator.get_page(page_number)

            uploaded_data = stockbalanceCreate.objects.all()

            for item in items_page:
                row_data = (
                    item.item_name,
                    item.item_code,
                    item.item_category,
                    item.item_group,
                    [],
                    item.stockbalancecreate_set.first().created_date
                    if item.stockbalancecreate_set.exists()
                    else None,
                    item.stockbalancecreate_set.first().update_date
                    if item.stockbalancecreate_set.exists()
                    else None,
                )
                for branch in branches:
                    stock_balance_item = branch.stockbalancecreate_set.filter(
                        item=item
                    ).first()
                    quantity = (
                        stock_balance_item.item_quantity if stock_balance_item else 0
                    )
                    row_data[4].append(quantity)
                stock_balance_data.append(row_data)

            return render(
                request,
                "stocks_balance.html",
                {
                    "stock_balance_data": stock_balance_data,
                    "branches": branches,
                    "uploaded_data": uploaded_data,
                    "items_page": items_page,  # Include the paginated items in the context
                },
            )
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


def upload_stock(request):
    if request.method == "POST":
        form = PosBulkUploadForm(
            request.POST, request.FILES
        )  # Replace with your actual form class
        if form.is_valid():
            file = request.FILES["file"]

            # Check the file type (CSV or Excel) and read data accordingly
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file)

            # Loop through the DataFrame and create stockbalanceCreate objects
            for index, row in df.iterrows():
                # Extract data from the DataFrame
                item_quantity = row["Quantity"]
                product_code = row["ProductCode"]
                # category = row['Category']  # Add this line to extract the Category value
                # group = row['Group']  # Add this line to extract the Group value

                # Map the product code to a valid item (product) ID in your database
                item_id = map_product_code_to_item_id(product_code)

                if item_id is None:
                    # Handle the case where the product code cannot be mapped
                    # You can log an error, skip the row, or take appropriate action here
                    continue

                stockbalanceCreate.objects.create(
                    item_quantity=item_quantity,
                    item_id=item_id,
                )

            # Redirect to a success page or display a success message
            return redirect(
                "stocks_balance"
            )  # Replace 'success' with the URL name of your success page

    else:
        form = PosBulkUploadForm()  # Replace with your actual form class

    return render(request, "upload_stock.html", {"form": form})


def map_product_code_to_item_id(product_code):
    try:
        # Implement your logic to map product_code to a valid item (product) ID
        # For example, you can query your Item model based on product_code
        # and return the ID if a matching item (product) is found
        item = Item.objects.get(item_code=product_code)
        return item.id
    except Item.DoesNotExist:
        # Handle the case where the item (product) does not exist or cannot be mapped
        # You can log an error or return None as needed
        return None


def edit_stocks_balance(request, item_id):
    if request.user.is_authenticated:
        check_function_name = (
            "edit_stocks_balance"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            item = get_object_or_404(Item, item_code=item_id)
            stock_balance_item = stockbalanceCreate.objects.filter(item=item).last()

            if request.method == "POST":
                form = stockbalanceCreateForm(request.POST, instance=stock_balance_item)
                if form.is_valid():
                    form.save()
                    return redirect("stocks_balance")
            else:
                form = stockbalanceCreateForm(instance=stock_balance_item)

            context = {
                "form": form,
                "item": item,
            }
            return render(request, "edit_stocks_balance.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")




# purchase order
def StockEntry_withPO(request):
    if request.user.is_authenticated:
        check_function_name = (
            "StockEntry_withPO"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                try:
                    search_po = request.POST.get("search_po")
                    if search_po == "search_po":
                        search_po_id = request.POST.get("po_no")
                        purchase_order = Purchase_Order.objects.filter(
                            po_number=search_po_id
                        )
                        context = {"purchase_order": purchase_order}
                        return render(request, "StockEntry_withPO.html", context)

                except Exception as error:
                    return render(request, "error.html", {"error": error})
            else:
                return render(request, "StockEntry_withPO.html")
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


# def edit_purchase_order(request, purchase_order_id):
#     purchase_order = get_object_or_404(Purchase_Order, id=purchase_order_id)
#     items = Item.objects.all()
#     uoms = UOM.objects.all()
#     suppliers = Supplier.objects.all()
#     branches = Branch.objects.all()

#     if request.method == "POST":
#         supplier_id = request.POST.get("mainItem")
#         supplier = Supplier.objects.get(id=supplier_id)
#         branch_id = request.POST.get("branch")
#         branch = Branch.objects.get(id=branch_id)
#         ingredients_list = list(request.POST.getlist("ingredient"))
#         uom_list = list(request.POST.getlist("mainUOM"))
#         quantity_list = list(request.POST.getlist("quantity"))
#         unit_price_list = list(request.POST.getlist("unit_price"))
#         quantity_added_list = list(request.POST.getlist("quantity_added"))

#         purchase_order.supplier = supplier
#         purchase_order.branch_name = branch
#         purchase_order.ingredients.clear()

#         for i in range(len(ingredients_list)):
#             ingredient = Item.objects.get(id=int(ingredients_list[i]))
#             uom = UOM.objects.get(id=int(uom_list[i]))
#             quantity = int(quantity_list[i])
#             unit_price = float(unit_price_list[i])
#             quantity_added = int(quantity_added_list[i])

#             new_ingredient = Ingredient.objects.create(
#                 main_item=ingredient, item=ingredient, item_UOM=uom, quantity=quantity, unit_price=unit_price
#             )
#             purchase_order.ingredients.add(new_ingredient)  # Associate the ingredient with the purchase order

#             # Update stock balance for the branch and ingredient
#             branch_item, created = stockbalanceCreate.objects.get_or_create(item=ingredient, branch=branch)
#             branch_item.item_quantity += quantity_added
#             branch_item.save()

#         purchase_order.save()
#         purchase_orders = Purchase_Order.objects.all()  # Update purchase_orders
#         context = {
#             "purchase_order": purchase_order,
#             "items": items,
#             "uoms": uoms,
#             "suppliers": suppliers,
#             "branches": branches,
#             "purchase_orders": purchase_orders,  # Include updated purchase orders
#         }

#         return redirect("/show_stock_receipts")
#     else:
#         form = Purchase_OrderForm()


#     context = {
#         # "stock_receipt":stock_receipt,
#         "purchase_order": purchase_order,
#         "items": items,
#         "uoms": uoms,
#         "suppliers": suppliers,


#         "branches": branches,
#         "purchase_orders": Purchase_Order.objects.all(),
#         "form":form
#     }
#     return render(request, "edit_purchase_order.html", context)


# Confirm Purchase Order to Stocks
def edit_purchase_order(request, purchase_order_id):
    purchase_order = get_object_or_404(Purchase_Order, id=purchase_order_id)
    items = Item.objects.all()
    uoms = UOM.objects.all()
    suppliers = Supplier.objects.all()
    branches = Branch.objects.all()

    if request.method == "POST":
        supplier_id = purchase_order.supplier_id
        branch_id = purchase_order.branch_name_id
        ingredients_list = purchase_order.ingredients.all()

        unit_price = request.POST.get(
            "unit_price"
        )  # Retrieve unit_price from POST data
        quantity_added = request.POST.get(
            "quantity_added"
        )  # Retrieve quantity_added from POST data

        new_receipt = Stock_Receipt.objects.create(
            supplier_id=supplier_id,
            branch_name_id=branch_id,
            receive_by=request.user,
        )

        for ingredient in ingredients_list:
            new_ingredient = Ingredient.objects.create(
                main_item=ingredient.main_item,
                item=ingredient.item,
                item_UOM=ingredient.item_UOM,
                quantity=quantity_added,
                unit_price=unit_price,  # Assign unit_price from POST data
                total_price=Decimal(quantity_added)
                * Decimal(unit_price),  # Calculate total price
            )
            new_receipt.ingredients.add(new_ingredient)

            # Update stock balance for the branch and ingredient
            branch_item, created = stockbalanceCreate.objects.get_or_create(
                item=ingredient.item, branch=branch_id
            )
            branch_item.item_quantity += ingredient.quantity
            branch_item.save()

        return redirect("show_stock_receipts")

    context = {
        "purchase_order": purchase_order,
        "items": items,
        "uoms": uoms,
        "suppliers": suppliers,
        "branches": branches,
        "purchase_orders": Purchase_Order.objects.all(),
    }
    return render(request, "edit_purchase_order.html", context)


def display_purchase_orders(request):
    if request.user.is_authenticated:
        check_function_name = (
            "display_purchase_orders"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            purchase_orders = Purchase_Order.objects.all()
            stock_receipts = Stock_Receipt.objects.select_related("purchase_order")

            context = {
                "purchase_orders": purchase_orders,
                "stock_receipts": stock_receipts,
            }

            return render(request, "display_purchase_orders.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


def StockEntry_withPO_edit(request, stock_receipt_id):
    if request.user.is_authenticated:
        check_function_name = (
            "StockEntry_withPO_edit"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            stock_receipt = get_object_or_404(Stock_Receipt, id=stock_receipt_id)

            if request.method == "POST":
                form = Stock_ReceiptForm(request.POST, instance=stock_receipt)
                if form.is_valid():
                    form.save()
                    return redirect(
                        "view_stock_receipt", stock_receipt_id=stock_receipt_id
                    )
            else:
                form = Stock_ReceiptForm(instance=stock_receipt)

            context = {
                "stock_receipt": stock_receipt,
                "form": form,
            }
            return render(request, "StockEntry_withPO_edit.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


def get_purchase_order_data(request):
    if (
        request.method == "GET"
        and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
    ):
        po_id = request.GET.get("po_id")
        try:
            purchase_order = Purchase_Order.objects.get(id=po_id)
            data = {
                "supplier_id": purchase_order.supplier_id,
                "branch_name_id": purchase_order.branch_name_id,
                "receive_by": purchase_order.receive_by,
                "items": [
                    {
                        "id": ingredient.item.id,
                        "uom_id": ingredient.item_UOM.id,
                        "quantity": ingredient.quantity,
                        "unit_price": ingredient.unit_price,
                    }
                    for ingredient in purchase_order.ingredients.all()
                ],
            }
            return JsonResponse(data)
        except Purchase_Order.DoesNotExist:
            pass

    return JsonResponse({"items": []})


def get_items(request):
    branch_id = request.GET.get("branch_id")
    items = stockbalanceCreate.objects.filter(branch_id=branch_id)
    item_list = []

    for item in items:
        item_data = {"id": item.id, "item_name": item.item.item_name}
        item_list.append(item_data)

    return JsonResponse({"items": item_list})


def StockEntry_withoutPO(request):
    form = Stock_ReceiptForm()
    supplier_form = SupplierForm()
    uoms = UOM.objects.all()
    suppliers = Supplier.objects.all()
    branches = Branch.objects.all()
    supplier_form = SupplierForm()  # Create an instance of the SupplierForm

    if request.method == "POST":
        # Create an instance of SupplierForm with the POST data
        supplier_form = SupplierForm(request.POST)
        if supplier_form.is_valid():
            # If the form is valid, save the supplier data
            supplier_form.save()
        branch_id = request.POST.get("branch")
        receive_by = request.POST.get("receive_by")
        ingredients_list = list(request.POST.getlist("ingredient"))
        uom_list = list(request.POST.getlist("mainUOM"))
        quantity_list = list(request.POST.getlist("quantity"))
        unitprices_list = request.POST.getlist("unit_price")

        try:
            branch = get_object_or_404(Branch, id=branch_id)
            supplier_id = int(request.POST.get("supplier"))
            supplier = get_object_or_404(Supplier, id=supplier_id)
        except (ValueError, Branch.DoesNotExist):
            return render(
                request, "error_template.html", {"message": "Invalid Branch ID"}
            )
        except Supplier.DoesNotExist:
            return render(
                request, "error_template.html", {"message": "Invalid Supplier ID"}
            )

        new_Purchase_Order = Stock_Receipt.objects.create(
            supplier=supplier, receive_by=receive_by, branch_name=branch
        )

        for i in range(len(ingredients_list)):
            ingredient_id = int(ingredients_list[i])
            uom = get_object_or_404(UOM, id=int(uom_list[i]))
            quantity = int(quantity_list[i])
            unit_price = Decimal(unitprices_list[i])
            ingredient = get_object_or_404(
                stockbalanceCreate, id=ingredient_id, branch=branch
            )
            print("quantity before:", ingredient.item_quantity)
            item_quantity = ingredient.item_quantity + quantity
            print("quantity after:", item_quantity)
            ingredient.item_quantity = item_quantity
            ingredient.save()

            ingredient.receveive_quantity = quantity

            total_price = Decimal(unit_price) * quantity
            newStockReceip_withoutPO = Ingredient.objects.create(
                main_item=new_Purchase_Order.item,
                item=ingredient.item,
                item_UOM=uom,
                quantity=quantity,
                total_price=total_price,
                unit_price=unit_price,
            )

            newStockReceip_withoutPO.item.save()

            new_Purchase_Order.ingredients.add(newStockReceip_withoutPO)

        return redirect("show_stock_receipts")

    context = {
        "form": form,
        "supplier_form": supplier_form,
        "uoms": uoms,
        "suppliers": suppliers,
        "branches": branches,
        "purchase_orders": Stock_Receipt.objects.all(),  # Include this to pass the purchase orders to the template
    }

    return render(request, "StockEntry_withoutPO.html", context)


def show_stock_receipts2(request, stock_receipt_id):
    stock_receipt = get_object_or_404(Stock_Receipt, id=stock_receipt_id)
    branches = Branch.objects.all()
    ingredients = Ingredient.objects.all()
    stock_receipts = Stock_Receipt.objects.all()
    if request.method == "POST":
        price = request.POST.get("price")
        received_by = request.POST.get("received_by")

        stock_receipt.price = price
        stock_receipt.received_by = received_by
        stock_receipt.save()

        return redirect("stock_receipt_detail", stock_receipt_id=stock_receipt.id)

    else:
        context = {"stock_receipt": stock_receipt}
        return render(request, "StockEntry_withPO_edit.html", context)


def stock_receipt_detail(request, stock_receipt_id):
    stock_receipt = get_object_or_404(Stock_Receipt, id=stock_receipt_id)

    context = {"stock_receipt": stock_receipt}
    return render(request, "stock_receipt_detail.html", context)


def show_stock_receipts(request):
    if request.user.is_authenticated:
        check_function_name = (
            "show_stock_receipts"  # Change this to the appropriate function name
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            branches = Branch.objects.all()
            ingredients = Ingredient.objects.all()
            stock_receipts = Stock_Receipt.objects.all()
            purchase_orders = (
                Purchase_Order.objects.all()
            )  # Retrieve all purchase orders
            purchase_orders = Stock_Receipt.objects.all()
            context = {
                "branches": branches,
                "ingredients": ingredients,
                "stock_receipts": stock_receipts,
                "purchase_orders": purchase_orders,  # Include purchase orders in context
            }
            return render(request, "show_stock_receipts.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")





def update_stock_receipt(request, stock_receipt_id):
    stock_receipt = get_object_or_404(Stock_Receipt, id=stock_receipt_id)

    if request.method == "POST":
        form = Stock_ReceiptForm(request.POST, instance=stock_receipt)
        if form.is_valid():
            form.save()  # Save the updated stock receipt details
            return redirect(
                "show_stock_receipts"
            )  # Redirect to the list of stock receipts
    else:
        form = Stock_ReceiptForm(instance=stock_receipt)

    context = {
        "form": form,
        "stock_receipt": stock_receipt,
    }

    return render(request, "update_stock_receipt.html", context)


def delete_stock_receipt(request, stock_receipt_id):
    stock_receipt = get_object_or_404(Stock_Receipt, id=stock_receipt_id)
    stock_receipt.delete()
    return render(request,"delete_stock_receipt.html")






# def get_items(request):
#     branch_id = request.GET.get('branch_id')
#     items = stockbalanceCreate.objects.filter(branch_id=branch_id)
#     item_list = []

#     for item in items:
#         item_data = {
#             'id': item.id,
#             'item_name': item.item.item_name
#         }
#         item_list.append(item_data)

#     return JsonResponse({'items': item_list})


# def StockEntry_withoutPO(request):
#     form = Stock_ReceiptForm()
#     uoms = UOM.objects.all()
#     suppliers = Supplier.objects.all()
#     branches = Branch.objects.all()

#     if request.method == "POST":
#         receive_by = request.POST.get("receive_by")
#         supplier = Supplier.objects.get(id=request.POST.get("mainItem"))
#         branch_id = request.POST.get("branch")
#         branch = Branch.objects.get(id=branch_id)

#         # Get the data from the POST request after obtaining branch and other details
#         ingredients_list = list(request.POST.getlist("ingredient"))
#         uom_list = list(request.POST.getlist("mainUOM"))
#         quantity_list = list(request.POST.getlist("quantity"))
#         unitprices_list = request.POST.getlist('unit_price')

#         new_Purchase_Order = Stock_Receipt.objects.create(
#             supplier=supplier, receive_by=receive_by, branch_name=branch
#         )

#         for i in range(len(ingredients_list)):
#             ingredient_id = int(ingredients_list[i])
#             uom = UOM.objects.get(id=int(uom_list[i]))
#             quantity = int(quantity_list[i])
#             unit_price = Decimal(unitprices_list[i])

#             # Use the branch_name field to filter ingredients associated with the selected branch
#             ingredient = stockbalanceCreate.objects.filter(branch=branch, item__id=ingredient_id).first()
#             if ingredient is None:
#                 continue

#             print("quantity before:", ingredient.item_quantity)
#             item_quantity = ingredient.item_quantity + quantity
#             print("quantity after:", item_quantity)
#             ingredient.item_quantity = item_quantity
#             ingredient.save()

#             ingredient.receveive_quantity = quantity

#             total_price = Decimal(unit_price) * quantity
#             newStockReceip_withoutPO = Ingredient.objects.create(
#             item=ingredient, item_UOM=uom, quantity=quantity,
#             total_price=total_price, unit_price=unit_price
#            )


#             print("quantity after:", item_quantity)
#             newStockReceip_withoutPO.main_item = new_Purchase_Order.item

#             newStockReceip_withoutPO.item.save()

#             new_Purchase_Order.ingredients.add(newStockReceip_withoutPO)

#         return redirect("show_stock_receipts")

#     context = {
#         "form": form,
#         "uoms": uoms,
#         "suppliers": suppliers,
#         "branches": branches,
#     }

#     return render(request, 'StockEntry_withoutPO.html', context)


def update_purchase(request, po_number):
    purchase_order = get_object_or_404(Purchase_Order, po_number=po_number)
    items = Item.objects.all()
    uoms = UOM.objects.all()
    suppliers = Supplier.objects.all()
    branches = Branch.objects.all()
    form = Purchase_OrderForm()

    if request.method == "POST":
        supplier_id = request.POST.get("mainItem")
        supplier = Supplier.objects.get(id=supplier_id)
        branch_id = request.POST.get("branch")
        branch = Branch.objects.get(id=branch_id)
        ingredients_list = list(request.POST.getlist("ingredient"))
        uom_list = list(request.POST.getlist("mainUOM"))
        quantity_list = list(request.POST.getlist("quantity"))
        unit_price_list = list(request.POST.getlist("unit_price"))

        purchase_order.supplier = supplier
        purchase_order.branch_name = branch
        purchase_order.ingredients.all().delete()  # Clear existing ingredients

        for i in range(len(ingredients_list)):
            ingredient = Item.objects.get(id=int(ingredients_list[i]))
            uom = UOM.objects.get(id=int(uom_list[i]))
            quantity = int(quantity_list[i])
            unit_price = float(unit_price_list[i])
            new_ingredient = Ingredient.objects.create(
                main_item=ingredient,
                item=ingredient,
                item_UOM=uom,
                quantity=quantity,
                unit_price=unit_price,
            )
            purchase_order.ingredients.add(new_ingredient)

        purchase_order.save()
        messages.success(request, "Successfully updated purchase order")
        return redirect("/show_purchase_order")
    else:
        form = Purchase_OrderForm()

    context = {
        "purchase_order": purchase_order,
        "items": items,
        "uoms": uoms,
        "suppliers": suppliers,
        "branches": branches,
        "form": form,
    }
    return render(request, "update_purchase.html", context)


# get item assign to branch


# calculate overdue days
def calculate_overdue_days(purchase_date, supplier):
    today = timezone.now().date()

    # Handling offset-naive and offset-aware datetime objects
    if timezone.is_aware(purchase_date):
        purchase_date = purchase_date.date()

    due_date = purchase_date + timedelta(days=supplier.credit_days)
    overdue_days = (today - due_date).days

    return overdue_days


def Purchases(request):
    if request.user.is_authenticated:
        check_function_name = (
            "Purchases"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            purchase_orders = Stock_Receipt.objects.all()

            for order in purchase_orders:
                order.overdue_days = calculate_overdue_days(
                    order.purchase_date, order.supplier
                )

            return render(
                request, "Purchases.html", {"purchase_orders": purchase_orders}
            )
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users




def manage_payments(request):
    if request.user.is_authenticated:
        check_function_name = (
            "manage_payments"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            purchase_orders = Stock_Receipt.objects.all().annotate(
                total_sumed_prices=Sum("ingredients__total_price")
            )
            return render(
                request, "manage_payments.html", {"purchase_orders": purchase_orders}
            )
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


def pre_payment(request, purchase_order_id):
    if request.user.is_authenticated:
        check_function_name = (
            "pre_payment"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                form = PaymentReportsForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect(
                        "payment_reports"
                    )  # Redirect after successful submission
            else:
                form = PaymentReportsForm()
            return render(request, "pre_payment.html", {"form": form})
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users

    # Retrieve purchase order data based on purchase_order_id
    # You can use this data to populate the payment form

    context = {
        # Pass relevant data to the template
    }

    return render(request, "pre_payment.html", context)


# def pre_payment(request, purchase_order_id):
#     # Retrieve purchase order data based on purchase_order_id
#     purchase_order = get_object_or_404(Purchase_Order, id=purchase_order_id)

#     context = {
#         'purchase_order': purchase_order,  # Pass relevant purchase order data to the template
#     }

#     return render(request, 'pre_payment.html', context)
# def payment_reports(request):
#     purchase_order = PaymentReports.objects.all()

#     context = {
#      'purchase_order': purchase_order
#     }

#     return render(request, 'payment_reports.html', context)


def all_payments(request):
    # Retrieve all payment records from your database
    payments = (
        PaymentReports.objects.all()
    )  # Replace PaymentModel with your actual payment model

    return render(request, "payment_reports.html", {"payments": payments})


def payment_reports(request):
    if request.user.is_authenticated:
        check_function_name = (
            "payment_reports"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            payment_reports = (
                PaymentReports.objects.all()
            )  # Retrieve payment reports data
            context = {"payment_reports": payment_reports}
            return render(request, "payment_reports.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# def payment_form(request, purchase_order_id):
#     form = PaymentReportsForm()
#     if request.method == 'POST':
#         form = PaymentReportsForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('payment_reports')  # Redirect to payment reports page
#     else:
#         form = PaymentReportsForm()

#     context = {
#         'purchase_order_id': purchase_order_id,
#         'form': form,
#     }
#     return render(request, 'pre_payment.html', context)


def payment_form(request):
    if request.user.is_authenticated:
        check_function_name = (
            "payment_form"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                form = ItemGroupForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect(
                        "payment_reports_list"
                    )  # Redirect after successful submission
            else:
                form = ItemGroupForm()
            return render(request, "pre_payment.html", {"form": form})
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


def viewdetail(request, po_number):
    if request.user.is_authenticated:
        check_function_name = (
            "viewdetail"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            queryset = Purchase_Order.objects.filter(po_number=po_number)
            context = {
                "purchasedetails": queryset,
            }
            return render(request, "view_eachpurchase.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


def show_purchase_order(request):
    if request.user.is_authenticated:
        check_function_name = (
            "show_purchase_order"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            purchases = Purchase_Order.objects.all()
            context = {"purchases": purchases}
            return render(request, "show_purchase_order.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# get branch items
def get_branch_items(request):
    branch_id = request.GET.get("branch_id")
    print("Received branch_id:", branch_id)  # Debug statement
    try:
        branch = Branch.objects.get(id=branch_id)
        items = Item.objects.filter(branch_name=branch)
        data = {
            "items": [{"id": item.id, "item_name": item.item_name} for item in items]
        }
        return JsonResponse(data)
    except Branch.DoesNotExist:
        print("Branch not found in the database.")  # Debug statement
        return JsonResponse({"error": "Branch not found."}, status=400)


# add_purchase


def add_purchase_order(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_purchase_order"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = Purchase_OrderForm()
            items = Item.objects.all()
            uoms = UOM.objects.all()
            suppliers = Supplier.objects.all()
            branches = Branch.objects.all()

            if request.method == "POST":
                supplier_id = request.POST.get("mainItem")
                supplier = Supplier.objects.get(id=supplier_id)
                branch_id = request.POST.get("branch")
                branch = Branch.objects.get(id=branch_id)
                ingredients_list = list(request.POST.getlist("ingredient"))
                uom_list = list(request.POST.getlist("mainUOM"))
                quantity_list = list(request.POST.getlist("quantity"))

                new_Purchase_Order = Purchase_Order.objects.create(
                    supplier=supplier, branch_name=branch
                )

                for i in range(len(ingredients_list)):
                    ingredient = Item.objects.get(id=int(ingredients_list[i]))
                    uom = UOM.objects.get(id=int(uom_list[i]))
                    quantity = int(quantity_list[i])
                    new_ingredient = Ingredient.objects.create(
                        main_item=ingredient,
                        item=ingredient,
                        item_UOM=uom,
                        quantity=quantity,
                    )
                    new_Purchase_Order.ingredients.add(new_ingredient)
                return redirect("show_purchase_order")

            else:
                form = Purchase_OrderForm()

            context = {
                "form": form,
                "items": items,
                "uoms": uoms,
                "suppliers": suppliers,
                "branches": branches,
            }
            return render(request, "add_purchase_order.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def deletepurchase(request, po_number):
    if request.user.is_authenticated:
        check_function_name = (
            "deletepurchase"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            queryset = Purchase_Order.objects.get(po_number=po_number)
            if request.method == "POST":
                queryset.delete()
                return redirect("show_purchase_order")
            return render(request, "deletepurchaseorder.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


def search_single_PO(request, pk):
    return render(request, "")


# Confirmed POs
def confirm_po(request):
    return render(request, "")


def get_connected_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    connected_suppliers = supplier.connected_suppliers.all()
    supplier_list = [{"id": i.id, "name": i.name} for i in connected_suppliers]
    return JsonResponse(request, {"suppliers": supplier_list})


@login_required
def confirm_stock_transfer(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            check_function_name = (
                "confirm_stock_transfer"  # The function name corresponding to this view
            )
            access_functions = request.session.get("user_allowed_func", [])
            is_superuser = request.session.get("is_super_users", False)

            if check_function_name in access_functions or is_superuser:
                po_number = request.POST.get("po_number", None)
                stock = Stock_Receipt.objects.filter(po_number=po_number).first()

                context = {"stock": stock}

                return render(request, "confirm_stock_transfer.html", context)
            else:
                return render(
                    request,
                    "error.html",
                    {"message": "You don't have permission to access this page."},
                )
        else:
            return redirect(
                "login_views"
            )  # Redirect to the login page for unauthenticated users

    return render(request, "confirm_stock_transfer.html")


# To View Stocks


@login_required
def view_stock(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_stock"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            stocks = Stock_Receipt.objects.all()
            context = {"stocks": stocks}
            return render(request, "view_stock.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# To add request Stock
@login_required
def stock_request(request):
    if request.user.is_authenticated:
        check_function_name = (
            "stock_request"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = StockRequestForm()
            items = Item.objects.all()
            uoms = UOM.objects.all()
            orders = StockRequest.objects.all()

            if request.method == "POST":
                form = StockRequestForm(request.POST)
                if form.is_valid():
                    try:
                        form.save()
                        return redirect("view_stock_request")
                    except:
                        pass
            else:
                form = StockRequestForm()

            context = {
                "form": form,
                "items": items,
                "uoms": uoms,
                "orders": orders,
            }
            return render(request, "stock_request.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# To View Stocks request


@login_required
def view_stock_request(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_stock_request"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            requests = StockRequest.objects.all()
            context = {"requests": requests}

            return render(request, "view_stock_request.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


def show_stockreceip(request):
    header = "list of items"
    form = Purchase_OrdeSearchForm(request.POST or None)
    queryset = Purchase_Order.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == "POST":
        queryset = Purchase_Order.objects.filter(
            po_number__icontains=form["po_number"].value()
        )
        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, "stockentry.html", context)


# To Add Stock Entry


# To View Stock Entry
@login_required
def view_stock_entry(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_stock_entry"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            entries = StockEntry.objects.all()
            context = {"entries": entries}

            return render(request, "view_stock_entry.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# To add billed stock
@login_required
def billed_stock(request):
    if request.user.is_authenticated:
        check_function_name = (
            "billed_stock"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = BilledStockForm()
            items = Item.objects.all()
            uoms = UOM.objects.all()

            if request.method == "POST":
                form = BilledStockForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_billed_stock")
            else:
                form = BilledStockForm()

            context = {"form": form, "items": items, "uoms": uoms}
            return render(request, "billed_stock.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# To view billed stock
@login_required
def view_billed_stock(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_billed_stock"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            bills = BilledStock.objects.all()
            context = {"bills": bills}
            return render(request, "view_billed_stock.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# branch transfer


def fetch_items(request):
    branch_id = request.GET.get("branch_id")
    items = Item.objects.filter(branch__id=branch_id)
    item_list = []

    for item in items:
        item_data = {"id": item.id, "item_name": item.item_name}
        item_list.append(item_data)

    return JsonResponse(item_list, safe=False)


# get branch items
def get_items_for_branch(request):
    branch_id = request.GET.get("branch_id")
    items = stockbalanceCreate.objects.filter(branch_id=branch_id)
    item_list = []

    for item in items:
        item_data = {"id": item.id, "item_name": item.item.item_name}
        item_list.append(item_data)

    return JsonResponse({"items": item_list})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Branch, Item, stockbalanceCreate, BranchTransfer


@login_required
def transfer_items(request):
    if request.user.is_authenticated:
        check_function_name = (
            "transfer_items"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            branches = Branch.objects.all()
            items = Item.objects.all()

            if request.method == "POST":
                from_branch_id = request.POST.get("from_branch")
                to_branch_id = request.POST.get("to_branch")

                item_ids = request.POST.getlist("item")
                quantities = request.POST.getlist("quantity")

                from_branch = Branch.objects.get(pk=from_branch_id)
                to_branch = Branch.objects.get(pk=to_branch_id)

                insufficient_items = []  # A list to store insufficient items

                with transaction.atomic():
                    for item_id, quantity in zip(item_ids, quantities):
                        item = Item.objects.get(pk=item_id)
                        quantity = int(quantity)

                        from_branch_item = stockbalanceCreate.objects.get_or_create(
                            branch=from_branch, item=item
                        )[0]
                        if from_branch_item.item_quantity < quantity:
                            insufficient_items.append(item.item_name)
                        else:
                            # Perform the quantity update only if there are enough items in the from_branch
                            from_branch_item.item_quantity -= quantity
                            from_branch_item.save()

                            # Update to_branch quantity
                            to_branch_item = stockbalanceCreate.objects.get_or_create(
                                branch=to_branch, item=item
                            )[0]
                            to_branch_item.item_quantity += quantity
                            to_branch_item.save()

                            # Create BranchTransfer record
                            BranchTransfer.objects.create(
                                from_branch=from_branch,
                                to_branch=to_branch,
                                item=item,
                                quantity=quantity,
                            )

                    if insufficient_items:
                        # Display a message for insufficient items
                        items_message = ", ".join(insufficient_items)
                        messages.error(
                            request,
                            f"The following items are insufficient: {items_message}",
                        )
                    else:
                        messages.success(request, "Items transferred successfully.")
                        return redirect("branch_transfer_items")

            return render(
                request,
                "transfer_items.html",
                {"branches": branches, "items": items},
            )
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def branch_transfer_items(request):
    if request.user.is_authenticated:
        check_function_name = (
            "branch_transfer_items"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            transfers = BranchTransfer.objects.all()
            context = {"transfers": transfers}
            return render(request, "show_branch_transfers.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Add_item_group
@login_required
def item_group(request):
    if request.user.is_authenticated:
        check_function_name = (
            "item_group"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                form = ItemGroupForm(request.POST)
                group_code = generate_itemgroup_code()
                if form.is_valid():
                    try:
                        new_itemgroup = form.save(commit=False)
                        new_itemgroup.group_code = group_code
                        new_itemgroup.save()
                        return redirect("view_item_group")
                    except:
                        pass
            else:
                form = ItemGroupForm()

            context = {"form": form}
            return render(request, "item_group.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# view_item_group
@login_required
def view_item_group(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_item_group"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            Item_groups = Item_group.objects.all()
            context = {"Item_groups": Item_groups}
            return render(request, "view_item_group.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# add_item_category
@login_required
def item_category(request):
    print("Item category")
    if request.user.is_authenticated:
        check_function_name = (
            "item_category"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                form = ItemCategoryForm(request.POST)
                if form.is_valid():
                    print("valid")
                    try:
                        last_record = Item_category.objects.last()
                        cat_code = last_record.category_code[3:]
                        print("000", cat_code)
                        category_code = generate_itemcategory(last_record.id)
                        print("category_code", category_code)
                        new_po = form.save(commit=False)
                        new_po.category_code = category_code
                        new_po.save()
                        return redirect("view_item_category")
                    except Exception as e:
                        # Print or log the error message for debugging
                        print("Error during form submission:", e)
                        # You can also pass the error message to the template to display it
                        context = {
                            "form": form,
                            "error_message": "An error occurred during form submission.",
                        }
                        return render(request, "item_category.html", context)
            else:
                form = ItemCategoryForm()

            context = {"form": form}
            return render(request, "item_category.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# view_item_category
@login_required
def view_item_category(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_item_category"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            Item_categories = Item_category.objects.all()
            context = {"Item_categories": Item_categories}
            return render(request, "view_item_category.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# item issue and updates

# end of items
from django.core.exceptions import ObjectDoesNotExist

# # add_bom
# def bom(request):
#     form = BOMForm()
#     items = Item.objects.all()
#     uoms = UOM.objects.all()
#     if request.method == "POST":
#         item = Item.objects.get(id=request.POST.get("mainItem"))
#         ingredients_list = list(request.POST.getlist("ingredient"))
#         uom_list = list(request.POST.getlist("mainUOM"))
#         quantity_list = list(request.POST.getlist("quantity"))

#         new_BOM = BOM.objects.create(item=item)
#          # Filter items to only include those with the "Finished Goods" category
#         finished_goods_category = Item_category.objects.get(category_name="Finished Goods")
#         finished_goods_items = Item.objects.filter(category=finished_goods_category)
#         try:
#             finished_goods_category = Item_category.objects.get(category_name="Finished Goods")
#         except ObjectDoesNotExist:
#             finished_goods_category = None  # Or provide a default category

#         finished_goods_items = Item.objects.filter(category=finished_goods_category)

#         for i in range(len(ingredients_list)):
#             ingredient = Item.objects.get(id=int(ingredients_list[i]))
#             uom = UOM.objects.get(id=int(uom_list[i]))
#             quantity = int(quantity_list[i])
#             new_ingredient = Ingredient.objects.create(
#                 main_item=item, item=ingredient, item_UOM=uom, quantity=quantity
#             )
#             new_BOM.ingredients.add(new_ingredient)
#         return redirect("view_bom")
#     else:
#         form = BOMForm()

#     context = {
#         "form": form,
#         # "items": finished_goods_items,  # Use the filtered items queryset
#         "items": items,
#         "uoms": uoms,
#     }
#     return render(request, "bom.html", context)


# def view_bom(request):
#     boms = BOM.objects.all()
#     context = {"boms": boms}
#     return render(request, "view_bom.html", context)
@login_required
def bom(request):
    if request.user.is_authenticated:
        check_function_name = "bom"  # The function name corresponding to this view
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = BOMForm()
            items = Item.objects.all()
            uoms = UOM.objects.all()

            if request.method == "POST":
                item = Item.objects.get(id=request.POST.get("mainItem"))
                ingredients_list = list(request.POST.getlist("ingredient"))
                uom_list = list(request.POST.getlist("mainUOM"))
                quantity_list = list(request.POST.getlist("quantity"))

                new_BOM = BOM.objects.create(item=item)

                for i in range(len(ingredients_list)):
                    ingredient = Item.objects.get(id=int(ingredients_list[i]))
                    uom = UOM.objects.get(id=int(uom_list[i]))
                    quantity = int(quantity_list[i])
                    new_ingredient = Ingredient.objects.create(
                        main_item=item, item=ingredient, item_UOM=uom, quantity=quantity
                    )
                    new_BOM.ingredients.add(new_ingredient)
                return redirect("view_bom")
            else:
                form = BOMForm()

            context = {
                "form": form,
                "items": items,
                "uoms": uoms,
            }
            return render(request, "bom.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_bom(request):
    if request.user.is_authenticated:
        check_function_name = "view_bom"  # The function name corresponding to this view
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            boms = BOM.objects.all()
            context = {"boms": boms}
            return render(request, "view_bom.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# view bom colum
@login_required
def view_bom_detail(request, bom_id):
    if request.user.is_authenticated:
        check_function_name = (
            "view_bom_detail"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            queryset = BOM.objects.filter(bom_id=bom_id)
            context = {
                "bomss": queryset,
            }
            return render(request, "view_eachbom.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def delete_bom(request, id):
    if request.user.is_authenticated:
        check_function_name = (
            "delete_bom"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            queryset = BOM.objects.get(id=id)
            if request.method == "POST":
                queryset.delete()
                return redirect("view_bom")

            return render(request, "deleteitems.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# to delete
def view_branchtranfer(request):
    branchese = BranchTransfer.objects.all()
    print(branchese)
    context = {"brancheses": branchese}
    return render(request, "view_stocktransfer.html", context)


# Add Company Details
@login_required
def add_company_details(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_company_details"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = Company_detailsForm()
            company_code = generate_company_code()
            if request.method == "POST":
                form = Company_detailsForm(request.POST)
                company_code = generate_company_code()
                if form.is_valid():
                    new_po = form.save(commit=False)
                    new_po.company_code = company_code
                    new_po.save()
                    form.save()
                    return redirect("company_details")
                else:
                    messages.info(request, message="Could not save company details")
                    return redirect("add_company_details")

            context = {"form": form}
            return render(request, "add_company_details.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# View Company Details
@login_required
def company_details(request):
    if request.user.is_authenticated:
        check_function_name = (
            "company_details"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            company_details = Company_details.objects.all()
            context = {"company_details": company_details}
            return render(request, "company_details.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Add Branch
@login_required
def branch(request):
    if request.user.is_authenticated:
        check_function_name = "branch"  # The function name corresponding to this view
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = BranchForm()

            if request.method == "POST":
                form = BranchForm(request.POST)
                branch_code = generate_Branch_code()
                if form.is_valid():
                    newbranch_code = form.save(commit=False)
                    newbranch_code.branch_code = branch_code
                    newbranch_code.save()
                    form.save()
                    return redirect("show_branch")
                else:
                    messages.info(request, message="Could not save branch")
                    return redirect("branch")

            context = {"form": form}
            return render(request, "branch.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


def access_denied(request):
    messages.error(request, "You don't have access to this page.")
    return render(
        request, "access_denied.html"
    )  # Create a template for the access denied message


# View Branch
@login_required
def show_branch(request):
    if request.user.is_authenticated:
        check_function_name = (
            "show_branch"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            branches = Branch.objects.all()
            context = {"branches": branches}
            return render(request, "show_branch.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# View UoM
@login_required
def UoM(request):
    if request.user.is_authenticated:
        check_function_name = "UoM"  # The function name corresponding to this view
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            uom = UOM.objects.all()
            context = {"uom": uom}
            return render(request, "UoM.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# List of Items
def list_of_items(request):
    items = Item.objects.all()
    print(items)
    context = {"items": items}
    return render(request, "list_of_items.html", context)


def request_payment(
    request, purchase_order_no, suppliername, phonenumber="254711123120"
):
    URL = BASE_URL + "purchase-order/"
    purchases = requests.get(
        URL, headers={"Accept": "application/json", "Content-Type": "application/json"}
    )

    URL = "http://bharathbrandsdotin.pythonanywhere.com/api/services/"
    data = {
        "service_id": "ST0033",
        "service_description": "Request Alada Payment",
        "total_fees": 100.0,
        "channel_id": "webfev011-2",
        "user_id": "1",
        "national_id": "232298",
        "phone_number": phonenumber,
        "service_type": "DirectServicePayment",
        "input_params_values": {
            "purchase_order_no": purchase_order_no,
            "supplier_name": suppliername,
            "total_fees": 100.0,
        },
    }
    response = requests.post(
        URL,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        data=json.dumps(data),
    )
    print(response.json())
    return redirect("manage_payments")


def loginPage(request):
    service_fields = get_service_fields("Login")
    service_metadata = get_service_metadata("Registration")
    National_ID = int("67889")
    if request.method == "POST":
        request.session["national_id"] = int("67889")
        # request.session['national_id']=request.POST.get('National_ID')
        National_ID = request.session["national_id"]
        data = request.POST
        print(data)
        request.session["captured_data"] = data
        print("login")
        response = transaction_login(data)
        if response == "AuthenticationFailed":
            print("response ", response)
            messages.error(request, "Invalid Credentials..!!")
            return redirect("loginPage")

        else:
            print("response ", response)
            return redirect("show_branch")
    captured_data = request.session.get("captured_data")
    # print("captured_data ", captured_data)
    context = {
        "service_fields": service_fields["service_fields"],
        "service_metadata": service_metadata,
        "National_ID": National_ID,
        "captured_data": captured_data,
    }
    return render(request, "login.html", context)


# Register
def registerPage(request):
    service_fields = get_service_fields("Registration")
    service_metadata = get_service_metadata("Registration")
    if request.method == "POST":
        data = request.POST
        response = all_transaction_process(data)  # calling transaction module
        if response == "failed":
            # print('Response ', response)
            messages.error(request, "please enter correct details")
            return redirect("registerPage")
        else:
            print("Response ", response)
            messages.success(request, "Please Login And Proceed Ahead..!!")
            return redirect("loginPage")
    context = {
        "service_fields": service_fields["service_fields"],
        "service_metadata": service_metadata,
    }
    return render(request, "register.html", context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(
                request, username=username, password=password
            )  # Pass the request to the authenticate function

            if user is not None:
                login(request, user)
                print("Tahnks")
                is_super_user = user.is_superuser
                print("is_super_user", is_super_user)
                try:
                    if is_super_user:
                        res = "is_superuser"
                        request.session["user_allowed_func"] = res
                        request.session["is_super_users"] = is_super_user
                    else:
                        user_role = (
                            user.user_role
                        )  # Access the user role through the user_role field
                        role_id = user_role.role_id
                        user_role_details = UserRole.objects.get(role_id=role_id)
                        user_details = user_role_details.functions_allowed
                        print("user details", user_details)
                        res = str(user_details).strip().split("<BBDelim>")
                        request.session["user_allowed_func"] = res
                        request.session["is_super_users"] = is_super_user
                except Exception as error:
                    print("error", error)
                return redirect("home")

            else:
                print("Invalid User")
                # Handle invalid login attempt here if needed
        else:
            print(form.errors)
            error = form.errors
            print("Error", error)
            context = {"form": form, "error": error}
            template_name = "login.html"
            return render(request, template_name, context)

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
        else:
            print("This is login views")
            form = AuthenticationForm()
            context = {
                "form": form,
            }
            template_name = "login.html"
            return render(request, template_name, context)


def error_page(request):
    template_name = "error.html"
    return render(request, template_name)


def app_function(request):
    if request.user.is_authenticated:
        check_function_name = "app_function"
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            all_glline = AppFunctions.objects.all().count()
            unique_fun_id = "FUN" + "0" + str(all_glline)
            form = AppFunctionsForm(initial={"function_id": unique_fun_id})

            if request.method == "POST":
                form = AppFunctionsForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect("/app_function")

            context = {"form": form, "all_all_gllineasset_type": all_glline}
            return render(request, "app_function.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


def create_user_view(request):
    if request.user.is_authenticated:
        check_function_name = "user_role"
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user_instance = form.save(commit=False)
                user_instance.user_ID = User.generate_stockreceipt_code()
                user_instance.set_password(
                    form.cleaned_data["password"]
                )  # Hashes the password
                user_instance.save()
                return redirect("user_list")
        else:
            form = UserCreationForm()

        users = User.objects.all()

    context = {
        "form": form,
        "users": users,
        "check_function_name": check_function_name,
        "access_functions": access_functions,
        "is_superuser": is_superuser,
    }
    return render(request, "create_user.html", context)


@login_required
def user_list_view(request):
    if request.user.is_authenticated:
        check_function_name = (
            "user_list_view"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            users = User.objects.all()  # Retrieve all User objects
            context = {"users": users}
            return render(request, "user_list.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


def app_function_view(request):
    if request.user.is_authenticated:
        check_function_name = (
            "app_function"  # Adjust this based on your permission logic
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            all_functions = AppFunctions.objects.all()  # Get all AppFunctions objects

            context = {
                "all_functions": all_functions,
            }
            return render(request, "all_app_functions.html", context)
        else:
            return redirect("error_page")  # Redirect to error page if not authorized
    else:
        return redirect("login_views")  # Redirect to login page if not authenticated


@login_required
def users(request):
    if request.user.is_authenticated:
        check_function_name = "users"  # The function name corresponding to this view
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "users.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def roles(request):
    if request.user.is_authenticated:
        check_function_name = "roles"  # The function name corresponding to this view
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "roles.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def functions(request):
    if request.user.is_authenticated:
        check_function_name = (
            "functions"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "functions.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# def user_role(request):
#     all_function = []
#     if request.user.is_authenticated:
#         check_function_name = "user_role"
#         access_functions = request.session.get("user_allowed_func", [])
#         is_superuser = request.session.get("is_super_users", False)

#         if check_function_name in access_functions or is_superuser:
#             if request.method == "POST":
#                 form = UserRoleForm(request.POST)
#                 if form.is_valid():
#                     role_id = form.cleaned_data["role_id"]
#                     role_name = form.cleaned_data["role_name"]

#                     allowed_functions = [
#                         func.function_name
#                         for func in AppFunctions.objects.all()
#                         if request.POST.get(func.function_name)
#                     ]
#                     final_allowed_func = ",".join(allowed_functions)

#                     data = UserRole(
#                         role_id=role_id,
#                         role_name=role_name,
#                         functions_allowed=final_allowed_func,
#                     )
#                     data.save()

#                     return redirect(
#                         "view_user_role"
#                     )  # Redirect after successful submission
#             else:
#                 all_glline = UserRole.objects.all().count()
#                 all_function = AppFunctions.objects.all()
#                 user_role_id = "UR" + "0" + str(all_glline)
#                 form = UserRoleForm(initial={"role_id": user_role_id})

#             context = {
#                 "form": form,
#                 "all_function": all_function,
#             }
#             return render(request, "user_role.html", context)
#         else:
#             return redirect("error_page")
#     else:
#         return redirect("login_views")


def user_role(request):
    if request.user.is_authenticated:
        check_function_name = "user_role"
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            all_glline = UserRole.objects.all().count()
            all_function = AppFunctions.objects.all()
            # user_role_id = 'UR' + '0' + str(all_glline)
            user_role_id = f"UR{all_glline + 1:02}"
            form = UserRoleForm(initial={"role_id": user_role_id})

            if request.method == "POST":
                form = UserRoleForm(request.POST)
                if form.is_valid():
                    role_id = form.cleaned_data["role_id"]
                    role_name = form.cleaned_data["role_name"]
                    all_function = AppFunctions.objects.all()
                    allowed_function = []

                    for func in all_function:
                        function_selected = request.POST.get(func.function_name)
                        if function_selected is not None:
                            allowed_function.append(
                                function_selected.strip() + "<BBDelim>"
                            )

                    final_allowed_func = " ".join(allowed_function)
                    data = UserRole(
                        role_id=role_id,
                        role_name=role_name,
                        functions_allowed=final_allowed_func,
                    )
                    data.save()

                    print(
                        f"Role Id : {role_id} | Role Name : {role_name} | allowed Function : {final_allowed_func}"
                    )

                    # Assuming you want to redirect to '/user_role' after saving
                    return HttpResponseRedirect("/user_role")

            context = {
                "form": form,
                "all_all_gllineasset_type": all_glline,
                "all_function": all_function,
            }
            return render(request, "user_role.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


def view_user_role(request):
    if request.user.is_authenticated:
        check_function_name = "user_role"
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            all_user_roles = (
                UserRole.objects.all()
            )  # Fetch all user roles from the database

            context = {
                "all_user_roles": all_user_roles,
            }
            return render(request, "view_user_role.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


def edit_user_role(request, role_id):
    if request.user.is_authenticated:
        check_function_name = (
            "edit_user_role"  # Replace with your actual permission check
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            user_role = get_object_or_404(UserRole, role_id=role_id)

            if request.method == "POST":
                form = UserRoleForm(request.POST, instance=user_role)
                if form.is_valid():
                    role = form.save(commit=False)
                    allowed_functions = [
                        func.function_name
                        for func in AppFunctions.objects.all()
                        if request.POST.get(func.function_name)
                    ]
                    role.functions_allowed = ",".join(allowed_functions)
                    role.save()
                    return redirect("view_user_role")

            else:
                all_function = AppFunctions.objects.all()
                # Split the functions_allowed data and convert it to a list
                user_role.functions_allowed = user_role.functions_allowed.split(",")
                form = UserRoleForm(instance=user_role)

            context = {
                "form": form,
                "all_function": all_function,
                "user_role": user_role,
            }
            return render(request, "edit_user_role.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


def delete_user_role(request, role_id):
    if request.user.is_authenticated:
        check_function_name = (
            "delete_user_role"  # Replace with your actual permission check
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            user_role = get_object_or_404(UserRole, role_id=role_id)

            if request.method == "POST":
                user_role.delete()
                return redirect("view_user_role")

            context = {
                "user_role": user_role,
            }
            return render(request, "delete_user_role.html", context)
        else:
            return redirect("error_page")
    else:
        return redirect("login_views")


# logout
def logoutUser(request):
    logout(request)
    return redirect("login_views")


@login_required
def profile(request):
    return redirect("home")


# SUPPLIER VIEWS
def supplier_mode(request):
    if request.session["mode"] == "supplier":
        request.session["mode"] = "client"
    elif request.session["mode"] == "client":
        request.session["mode"] = "supplier"
    return redirect("home")


# Gl LIne
@login_required
def add_gline(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_gline"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = GLLineForm()
            if request.method == "POST":
                form = GLLineForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_gline")
            else:
                form = GLLineForm()

            return render(request, "add_gline.html", {"form": form})
        else:
            return render(request, "error.html")
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_gline(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_gline"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            glines = GLLine.objects.all()
            return render(request, "view_gline.html", {"glines": glines})
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def all_gline(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_gline"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            context = {"add_account_type": "active"}
            return render(request, "all_gline.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Assert Type
@login_required
def add_asset_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_asset_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = AssetTypeForm()
            if request.method == "POST":
                form = AssetTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_asset_type")
            else:
                form = AssetTypeForm()

            return render(request, "add_asset_type.html", {"form": form})
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_asset_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_asset_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            assets = AssetType.objects.all()
            return render(request, "view_asset_type.html", {"assets": assets})
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def all_asset_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_asset_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            context = {"add_account_type": "active"}
            return render(request, "all_asset_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Account Type
@login_required
def add_account_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_account_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = AccountTypeForm()
            if request.method == "POST":
                form = AccountTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_account_type")
            else:
                form = AccountTypeForm()
            context = {"form": form, "add_account_type": "active"}
            return render(request, "add_account_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_account_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_account_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            accounts = AccountType.objects.all()
            return render(request, "view_account_type.html", {"accounts": accounts})
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def all_account_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_account_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "all_account_type.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Account


@login_required
def add_account(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_account"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = AccountForm()
            if request.method == "POST":
                form = AccountForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_account_type")
            else:
                form = AccountForm()
            context = {"form": form, "add_account": "active"}
            return render(request, "add_account.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_account(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_account"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            accounts = Account.objects.all()
            context = {"accounts": accounts}
            return render(request, "view_account.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def all_account(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_account"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "all_account.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Transaction


@login_required
def add_transaction(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_transaction"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = AccountForm()
            if request.method == "POST":
                form = AccountForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_account_type")
            else:
                form = AccountForm()
            context = {"form": form, "add_account": "active"}
            return render(request, "add_transaction.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_transaction(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_transaction"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            accounts = TransactionType.objects.all()
            context = {"accounts": accounts}
            return render(request, "view_transaction.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def all_transaction(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_transaction"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "all_transaction.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Transaction Code
@login_required
def add_transaction_code(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_transaction_code"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = TransactionCodeForm()
            if request.method == "POST":
                form = TransactionCodeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_transaction_code")
            else:
                form = TransactionCodeForm()
            context = {"form": form, "add_transaction_code": "active"}
            return render(request, "add_transaction_code.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_transaction_code(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_transaction_code"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            codes = ChargeType.objects.all()
            context = {"codes": codes}
            return render(request, "view_transcation_code.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Charge Type
@login_required
def add_charge_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_charge_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = ChargeTypeForm()
            if request.method == "POST":
                form = ChargeTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_charge_type")
            else:
                form = ChargeTypeForm()
            context = {"form": form, "add_charge_type": "active"}
            return render(request, "add_charge_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_charge_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_charge_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            types = TransactionCode.objects.all()
            context = {"types": types}
            return render(request, "view_charge_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Transaction Type
@login_required
def add_transaction_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_transaction_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = TransactionTypeForm()
            if request.method == "POST":
                form = TransactionTypeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_transaction_type")
            else:
                form = TransactionTypeForm()
            context = {"form": form, "add_transaction_type": "active"}
            return render(request, "add_transaction_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_transaction_type(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_transaction_type"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            types = TransactionType.objects.all()
            context = {"types": types}
            return render(request, "view_transaction_type.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Account Entry


def account_entry(member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id):
    try:
        entry_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        print("Account Entry Statement ...")
        print(member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id)

        # Debit account process
        dr_acc_detail = Account.objects.get(account_number=dr_acc)
        AccountEntry.objects.create(
            entry_ID=entry_id,
            transaction_ID=transaction_id,
            user_id=member_id,
            account_number_id=dr_acc,
            group_name_id=group_id,
            amount=-pay_amount,
            currency="KES",
            debit_credit_marker="Debit",
        )
        dr_acc_detail.current_cleared_balance -= float(pay_amount)
        dr_acc_detail.total_balance -= float(pay_amount)
        dr_acc_detail.save()
        print("Credit process.")

        # Credit account process
        entry_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        cr_acc_detail = Account.objects.get(account_number=cr_acc)
        AccountEntry.objects.create(
            entry_ID=entry_id,
            transaction_ID=transaction_id,
            user_id=member_id,
            account_number_id=cr_acc,
            group_name_id=group_id,
            amount=pay_amount,
            currency="KES",
            debit_credit_marker="Credit",
        )
        print("here...")
        cr_acc_detail.current_cleared_balance += float(pay_amount)
        cr_acc_detail.total_balance += float(pay_amount)
        cr_acc_detail.save()
        print("llllll")
        return True
    except Exception as error:
        print("error ", error)
        return False


@login_required
def account_entry_view(request):
    if request.user.is_authenticated:
        check_function_name = (
            "account_entry_view"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            if request.method == "POST":
                # Retrieve data from the form
                member_id = request.POST.get("member_id")
                group_id = request.POST.get("group_id")
                pay_amount = float(request.POST.get("pay_amount"))
                dr_acc = request.POST.get("dr_acc")
                cr_acc = request.POST.get("cr_acc")
                transaction_id = request.POST.get("transaction_id")

                # Call the account_entry function
                success = utils.account_entry(
                    member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id
                )

                if success:
                    return render(request, "account_success_template.html")
                else:
                    return render(request, "error_template.html")

            return render(request, "account_entry_form.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def add_account_entry(request):
    if request.user.is_authenticated:
        check_function_name = (
            "add_account_entry"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            form = AccountEntryForm()
            if request.method == "POST":
                form = AccountEntryForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("view_Account_entry")
            else:
                form = AccountEntryForm()
            context = {"form": form, "add_account": "active"}
            return render(request, "add_account_entry.html", context)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def view_account_entry(request):
    if request.user.is_authenticated:
        check_function_name = (
            "view_account_entry"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "view_account_entry.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


@login_required
def all_account_entry(request):
    if request.user.is_authenticated:
        check_function_name = (
            "all_account_entry"  # The function name corresponding to this view
        )
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "all_account_entry.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# POS


@login_required
def pos(request):
    if request.user.is_authenticated:
        check_function_name = "pos"  # The function name corresponding to this view
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            return render(request, "pos.html")
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# item bulk upload


def upload_sales(request):
    if request.method == "POST":
        form = PosBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]

            # Check the file type (CSV or Excel) and read data accordingly
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file)

            # Loop through the DataFrame and create Sale objects
            for index, row in df.iterrows():
                try:
                    # Retrieve the first matching Item instance based on the item name
                    item_name = row["ProductName"]
                    item = Item.objects.filter(item_name=item_name).first()

                    if item:
                        # Retrieve the Branch instance based on the branch name
                        branch_name = row["Branch"]
                        branch, _ = Branch.objects.get_or_create(
                            branch_name=branch_name
                        )

                        Sale.objects.create(
                            item=item,
                            receipt_number=row["TransactionCode"],
                            branch=branch,
                            quantity_sold=row["Quantity"],
                            unit_price=row["SellPrice"],
                            # Add other fields as needed
                        )
                except Item.DoesNotExist:
                    # Handle the case when the item is not found
                    pass

            # Redirect to a success page or display a success message
            return redirect("view_sales")

    else:
        form = PosBulkUploadForm()

    return render(request, "upload_sales.html", {"form": form})


def add_sales(request):
    if request.method == "POST":
        receipt_number = generate_receipt_number()
        form = SaleForm(request.POST)

        if form.is_valid():
            sale = form.save(
                commit=False
            )  # Save the sale but don't commit it to the database yet
            sale.total_amount = sale.unit_price * sale.quantity_sold

            try:
                stock_balance = stockbalanceCreate.objects.get(
                    branch=sale.branch,
                    item=sale.item,
                )
                # Check if there are enough items in stock
                if stock_balance.item_quantity >= sale.quantity_sold:
                    stock_balance.item_quantity -= sale.quantity_sold
                    stock_balance.save()
                else:
                    # Insufficient items, display a message
                    messages.error(request, "Insufficient items in stock.")
                    return redirect("add_sales")  # Redirect back to the sales form
            except stockbalanceCreate.DoesNotExist:
                # Handle the case where stock balance does not exist for the branch and item
                messages.error(
                    request,
                    "Stock balance not found for this item and branch. Try again..",
                )
                return redirect("add_sales")  # Redirect back to the sales form

            # Set the receipt number and save the sale to the database
            sale.receipt_number = receipt_number
            sale.save()

            return redirect(
                "view_sales"
            )  # Redirect to the view_sales page after submitting the form

    else:
        form = SaleForm()

    context = {"form": form}
    return render(request, "add_sales.html", context)


# def view_sales(request):
#     # Get the search query from the form input
#     search_query = request.GET.get('search_query')
#     sort_by = request.GET.get(
#         "sort_by", "created_date"
#     )  # Default to sorting by created_date if not provided
#     sort_order = request.GET.get(
#         "sort_order", "asc"
#     )  # Default to ascending order if not provided
#     # Filter sales records based on the search criteria
#         # Sorting logic based on the column clicked
#     if sort_by == "item_name":
#         items = items.order_by(
#             "item_name" if sort_order == "asc" else "-item_name"
#         )
#     elif sort_by == "item_code":
#         items = items.order_by(
#             "item_code" if sort_order == "asc" else "-item_code"
#         )
#     if search_query:
#         # Use Q objects to perform OR-based filtering
#         sales = Sale.objects.filter(
#             Q(item__item_name__icontains=search_query) |  # Search by item name
#               # Search by item code (assuming itemcode is the field in the Item model)
#             Q(branch__branch_name__icontains=search_query)  # Search by branch name
#         )
#     else:
#         # If no search query is provided, fetch all sales records
#         sales = Sale.objects.all()

#     context = {'sales': sales}
#     return render(request, 'view_sales.html', context)


from django.db.models import Q
from django.shortcuts import render
from .models import Sale  # Import the Sale model (adjust the import as needed)


def view_sales(request):
    # Get the search query from the form input
    search_query = request.GET.get("search_query")
    sort_by = request.GET.get(
        "sort_by", "sale_date"
    )  # Default to sorting by sale_date if not provided
    sort_order = request.GET.get(
        "sort_order", "desc"
    )  # Default to ascending order if not provided
    sales = Sale.objects.all()

    # Sorting logic based on the column clicked
    if sort_by == "item_name":
        sales = sales.order_by(
            "item__item_name" if sort_order == "desc" else "-item__item_name"
        )
    elif sort_by == "item_code":
        sales = sales.order_by(
            "item__item_code" if sort_order == "desc" else "-item__item_code"
        )
    elif sort_by == "branch_name":
        sales = sales.order_by(
            "branch__branch_name" if sort_order == "desc" else "-branch__branch_name"
        )

    # Filter sales records based on the search criteria
    if search_query:
        # Use Q objects to perform OR-based filtering
        sales = sales.filter(
            Q(item__item_name__icontains=search_query)
            | Q(branch__branch_name__icontains=search_query)
            | Q(receipt_number__icontains=search_query)
        )

    context = {"sales": sales}
    return render(request, "view_sales.html", context)


def get_suppliers():
    # Make the API call
    url = "http://bharathbrandsdotin.pythonanywhere.com/api-alada/register-supplier/"
    response = requests.get(url)

    if response.status_code == 200:
        # Extract the JSON response
        suppliers = response.json()
        return suppliers
    else:
        # Handle API error
        return []


def my_view(request):
    # Call the get_suppliers() function to fetch the list of suppliers
    suppliers = get_suppliers()

    # Pass the list of suppliers to the template context
    context = {"suppliers": suppliers}

    return render(request, "my_template.html", context)


@login_required
def pay(request, id):
    if request.user.is_authenticated:
        check_function_name = "pay"  # The function name corresponding to this view
        access_functions = request.session.get("user_allowed_func", [])
        is_superuser = request.session.get("is_super_users", False)

        if check_function_name in access_functions or is_superuser:
            cl = MpesaClient()

            po = (
                Stock_Receipt.objects.annotate(
                    total_sumed_prices=Sum("ingredients__total_price")
                )
                .filter(pk=id)
                .first()
            )

            phone_number = "0700805271"
            amount = int(po.total_sumed_prices)
            account_reference = "reference"
            transaction_desc = "Description"
            callback_url = "https://api.darajambili.com/express-payment"

            # Initiate the payment process using the MpesaClient
            response = cl.stk_push(
                phone_number, amount, account_reference, transaction_desc, callback_url
            )

            return HttpResponse(response)
        else:
            return render(
                request,
                "error.html",
                {"message": "You don't have permission to access this page."},
            )
    else:
        return redirect(
            "login_views"
        )  # Redirect to the login page for unauthenticated users


# Daraja view
def stk_push_callback(request):
    data = request.body
    return HttpResponse("STK Push in Django")


# Token  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
