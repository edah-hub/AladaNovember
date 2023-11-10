from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User
from django.utils.translation import gettext_lazy as _


class SupplierTypeForm(forms.ModelForm):
    class Meta:
        model = SupplierType
        fields = "__all__"
        exclude = ("amount",)


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class AppFunctionsForm(forms.ModelForm):
    class Meta:
        model = AppFunctions
        fields = [
            "function_id",
            "function_name",
            "purpose",
        ]  # Add the actual fields from your model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["function_id"].widget.attrs[
            "readonly"
        ] = True  # Make function_id readonly
        # Add any additional customization to form fields as needed


class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ["role_id", "role_name"]
        widgets = {
            "role_id": forms.TextInput(attrs={"readonly": "readonly"}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            "item",
            "branch",
            "quantity_sold",
            "unit_price",
        ]  # Include unit_price, exclude total_amount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_quantity_sold(self):
        quantity_sold = self.cleaned_data["quantity_sold"]
        stock_balance = stockbalanceCreate.objects.filter(
            branch=self.cleaned_data["branch"],
            item=self.cleaned_data["item"],
        ).first()
        if stock_balance and quantity_sold > stock_balance.item_quantity:
            raise forms.ValidationError("Quantity sold exceeds available stock.")
        return quantity_sold


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ["user_ID"]  # Exclude the user_ID field from the form
        fields = [
            "name",
            "user_role",
            "phone",
            "email",
            "department",
            "branch_code",
            "username",
            "password",
        ]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"


class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = "__all__"


class ChargeTypeForm(forms.ModelForm):
    class Meta:
        model = ChargeType
        fields = "__all__"


class GLLineForm(forms.ModelForm):
    class Meta:
        model = GLLine
        fields = "__all__"


class AccountTypeForm(forms.ModelForm):
    class Meta:
        model = AccountType
        fields = "__all__"


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"


class AccountEntryForm(forms.ModelForm):
    class Meta:
        model = AccountEntry
        fields = "__all__"


class TransactionCodeForm(forms.ModelForm):
    class Meta:
        model = TransactionCode
        fields = "__all__"


class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = "__all__"


class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = Item_category
        exclude = ("category_code",)

    def __init__(self, *args, **kwargs):
        super(ItemCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ItemGroupForm(forms.ModelForm):
    class Meta:
        model = Item_group
        exclude = ("group_code",)

    def __init__(self, *args, **kwargs):
        super(ItemGroupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class UOMForm(forms.ModelForm):
    class Meta:
        model = UOM
        fields = "__all__"


class stockbalanceCreateForm(forms.ModelForm):
    class Meta:
        model = stockbalanceCreate
        fields = [
            "item",
            "branch",
            "item_quantity",
        ]  # Adjust fields as needed


class PaymentReportsForm(forms.ModelForm):
    class Meta:
        model = PaymentReports
        fields = "__all__"


class Purchase_OrdeSearchForm(forms.ModelForm):
    class Meta:
        model = Purchase_Order
        fields = [
            "po_number",
        ]


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        exclude = ("branch_code",)


class Company_detailsForm(forms.ModelForm):
    class Meta:
        model = Company_details
        exclude = ("company_code",)


# Items


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["item_name", "item_category", "item_group", "item_UOM"]


class StocksBalanceForm(forms.Form):
    model = stockbalanceCreate
    item = forms.ModelChoiceField(queryset=Item.objects.all(), empty_label=None)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label=None)
    item_quantity = forms.IntegerField()


class UOMForm(forms.ModelForm):
    class Meta:
        model = UOM
        fields = "__all__"


class Purchase_OrderForm(forms.ModelForm):
    class Meta:
        model = Purchase_Order
        exclude = ["po_number", "unit_price"]
        widgets = {
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "branch_name": forms.Select(attrs={"class": "form-select"}),
            "item": forms.Select(attrs={"class": "form-select"}),
            "uomm": forms.Select(attrs={"class": "form-select"}),
            "purchase_quantity": forms.TextInput(attrs={"class": "form-control"}),
        }


class Stock_ReceiptForm(forms.ModelForm):
    class Meta:
        model = Stock_Receipt
        fields = "__all__"

    item_uom = forms.ModelChoiceField(
        queryset=UOM.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super(Stock_ReceiptForm, self).__init__(*args, **kwargs)
        self.fields["supplier"].widget = forms.Select(attrs={"class": "form-select"})
        self.fields["item"].widget = forms.Select(attrs={"class": "form-select"})
        self.fields["uomm"].widget = forms.Select(attrs={"class": "form-select"})

        # Pre-fill the item_uom and quantity fields based on the selected Purchase Order
        selected_purchase_order = kwargs.pop("selected_purchase_order", None)
        if selected_purchase_order:
            self.fields["item_uom"].initial = selected_purchase_order.uomm
            self.fields["quantity"].initial = selected_purchase_order.purchase_quantity


class BOMForm(forms.ModelForm):
    class Meta:
        model = BOM
        fields = "__all__"


class BranchTransferForm(forms.ModelForm):
    class Meta:
        model = BranchTransfer
        exclude = ("transfer_date",)


class StockRequestForm(forms.ModelForm):
    class Meta:
        model = StockRequest
        fields = "__all__"


class BilledStockForm(forms.ModelForm):
    class Meta:
        model = BilledStock
        fields = "__all__"


class UserRegistrationForm(UserCreationForm):
    role = forms.ModelChoiceField(queryset=UserRole.objects.all(), label="Select Role")
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2", "role"]


class ItemBulkUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload CSV/Excel File", help_text="Accepts CSV and Excel files"
    )


class PosBulkUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload CSV/Excel File", help_text="Accepts CSV and Excel files"
    )


class BulkUploadForm(forms.Form):
    file = forms.FileField(
        label="Upload CSV/Excel File", help_text="Accepts CSV and Excel files"
    )
