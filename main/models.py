
from django.db import models
from django.utils import timezone
from .utils import generate_bom_id
from django.db.models import Sum
import uuid
import datetime
import django.utils.timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    User,
    BaseUserManager,
    Group,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _



# defining  all the models


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide a valid email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
class UserRole(models.Model):
    role_id = models.CharField(max_length=10, null=False, blank=False, primary_key=True)
    role_name = models.CharField(max_length=200,unique=True)
    functions_allowed = models.TextField(editable=False, default='',null=True, blank=True)

    def __str__(self):
        return self.role_name
   
class Branch(models.Model):
    class Choose_Main_branch(models.TextChoices):
        Yes = "Yes", "Yes"
        No = "No", "No"
    branch_name = models.CharField(max_length=250, unique=True, null=True)
    branch_code =  models.CharField(max_length=20, unique=True)
    branch_location = models.CharField(max_length=200)
    main_branch = models.CharField(max_length=12, choices=Choose_Main_branch.choices, null=True)
    def __str__(self):
        return self.branch_name

class User(AbstractUser):
    user_ID = models.CharField(max_length=100, editable=False)
    name = models.CharField(max_length=100, null=True, blank=False) 
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='ul', null=True, blank=False) 
    phone = models.IntegerField(null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    department = models.CharField(max_length=100, null=True, blank=False)
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=False)


    def __str__(self):
        return self.user_ID    

    @staticmethod
    def generate_stockreceipt_code():
        last_stockreceipt = User.objects.order_by('-user_ID').first()
        if last_stockreceipt: 
            listIndex = len(last_stockreceipt.user_ID.split('-'))
            last_stockreceipt_number = int(last_stockreceipt.user_ID.split('-')[listIndex-1].strip()[2:])  # Extract the numeric part
            new_stockreceipt_number = last_stockreceipt_number + 1
        else:
            new_stockreceipt_number = 1
        user_ID = f"SU-{str(new_stockreceipt_number).zfill(3)}"  # Format with leading zeros
        return user_ID
    def save(self, *args, **kwargs):
            if not self.user_ID:
                self.user_ID = User.generate_stockreceipt_code()
            super(User, self).save(*args, **kwargs)


class AppFunctions(models.Model):
    function_id = models.CharField(max_length=100, primary_key=True, blank=False, null=False)
    function_name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100, blank=True, null=False)

    


class Company_details(models.Model):
    class Choose_payment(models.TextChoices):
        PHONE = "Phone Number", "Phone Number"
        PAYBILL = "Paybill", "Paybill"
        TILL = "Till", "Till"
        CASH = "Cash", "Cash"
    company_name = models.CharField(max_length=250, ) #unique=True
    company_code = models.CharField(max_length=20, unique=True)
    company_location = models.CharField(max_length=255)
    preffered_mode_of_payment = models.CharField(max_length=255, choices=Choose_payment.choices, null=True)
    till_number = models.IntegerField()
    paybill_number = models.IntegerField()
    
    def __str__(self):
        return self.company_name
       



# Create your models here.
class SupplierType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    class ModeOfPayments(models.TextChoices):
        PHONE = "Phone Number", "Phone Number"
        PAYBILL = "Paybill", "Paybill"
        TILL = "Till", "Till"
        CASH = "Cash", "Cash"
        
    supplier_name = models.CharField(max_length=250)
    supplier_type = models.ForeignKey(SupplierType, on_delete=models.CASCADE, related_name='supplier_supplier_type')
    preferred_mode_of_payment = models.CharField(max_length=12, choices=ModeOfPayments.choices, null=True)
    physical_location = models.CharField(max_length=100)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=13)
    credit_days = models.IntegerField()
    def __str__(self):
        return self.supplier_name
    

class Item_category(models.Model):
    category_name = models.CharField(max_length=250,unique=True,)
    category_code = models.CharField(max_length=250, unique=True,)

    def __str__(self):
        return self.category_name

class Item_group(models.Model):
    group_name = models.CharField(max_length=250,unique=True,)
    group_code = models.CharField(max_length=250,unique=True,)
    

    def __str__(self):
        return self.group_name
    
class UOM(models.Model):   
    UOM_name = models.CharField(max_length=250)

    def __str__(self):
        return self.UOM_name
    


        
class Item(models.Model):
    item_name = models.CharField(max_length=250)
    item_code = models.CharField(max_length=255, unique=True,)
    item_category = models.ForeignKey(Item_category,on_delete=models.CASCADE, related_name='item_category')
    item_group = models.ForeignKey(Item_group,on_delete=models.CASCADE, related_name='item_group')
    item_UOM = models.ForeignKey(UOM, on_delete=models.CASCADE, related_name='item_uom')
    receveive_quantity =models.CharField(max_length=50, blank=True, null=True)
    receive_by =models.CharField(max_length=50, blank=True, null=True)
    issue_quantity =models.CharField(max_length=50, blank=True, null=True)
    issue_by =models.CharField(max_length=50, blank=True, null=True)
    issue_to =models.CharField(max_length=50, blank=True, null=True)
    created_by =models.CharField(max_length=50, blank=True, null=True)
    reorder_level =models.IntegerField(default='0',  blank=True, null=True)
    last_updated =models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True, auto_now=False)
   
   

    def __str__(self):
        return self.item_name
    @staticmethod
    def generate_itemcode():
        last_item = Item.objects.order_by('-item_code').first()
        if last_item:
            last_code = last_item.item_code.split('-')[-1]
            last_three_digits_itemcode = int(last_code)
        else:
            last_three_digits_itemcode = 0

        last_three_digits_itemcode += 1
        category_code = 'ITCODE-00-' + str(last_three_digits_itemcode).zfill(3)
        return category_code
    


class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    receipt_number =  models.CharField(max_length=20, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default = 0)  # Add unit price field
    sale_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Keep total_amount nullable

    def calculate_total_amount(self):
        if self.unit_price is not None:
            return self.unit_price * self.quantity_sold
        else:
            return None

    def save(self, *args, **kwargs):
        # Calculate the total_amount before saving
        self.total_amount = self.calculate_total_amount()
        super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.item)





class stockbalanceCreate(models.Model):
    item_quantity = models.IntegerField(null=True, blank=True, default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Add this field for the date of creation
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)  # Add this field for the date of creation
    class Meta:
        unique_together = ('branch', 'item')
        
    def __str__(self):
        return self.item.item_name

class Ingredient(models.Model):
    main_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='ingredients_items_two', null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='ingredients_items', null=True)
    item_UOM = models.ForeignKey(UOM, on_delete=models.CASCADE, related_name='item_uom_ingredients')
    quantity = models.IntegerField(null=True)
    unit_price = models.DecimalField(max_digits=210, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=210, decimal_places=2, null=True)
    
    def __str__(self):
        return str(self.item)
    
    

class Purchase_Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    branch_name = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='purchase_branch')
    po_number = models.CharField(max_length=255, unique=True)
    # item = models.ForeignKey(Item, related_name='po_item_name', on_delete=models.CASCADE, null=True)
    # uomm = models.ForeignKey(UOM, related_name='po_UOMM', on_delete=models.CASCADE, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='PO_ing', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    purchase_quantity = models.CharField(max_length=13)
    purchase_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(auto_now_add=False, auto_now=True)
   

    def save(self, *args, **kwargs):
        # Calculate the unit_price based on the selected item
        if self.item:
            ingredient = Ingredient.objects.filter(main_item=self.item).first()
            if ingredient:
                self.unit_price = ingredient.unit_price
        super().save(*args, **kwargs)

    @property
    def unit_price(self):
        if self.ingredients.exists():
            return self.ingredients.first().unit_price
        return None

    def __str__(self):
        return self.po_number

    def save(self, *args, **kwargs):
        if not self.po_number:
            self.po_number = generate_po_code()
        super().save(*args, **kwargs)



def generate_po_code():
    last_ponumber = Purchase_Order.objects.order_by('-id').first()
    if last_ponumber:
        last_ponumber_id = int(last_ponumber.po_number.split('-')[2].strip())
        new_ponumber_id = last_ponumber_id + 1
    else:
        new_ponumber_id = 1
    po_number = f"PO-NUM-{str(new_ponumber_id).zfill(3)}"
    return po_number




class Stock_Receipt(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirm', 'Confirm'),
    )
    orderstatus = models.CharField(max_length=500, null=True, choices=ORDER_STATUS_CHOICES, default='pending')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True,)
    branch_name = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='purchase_orders')
    stockreip = models.CharField(max_length=255, unique=True,)
    phone_number = models.CharField(max_length=500, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    item = models.ForeignKey(Item, related_name='po_item', on_delete=models.CASCADE, null=True)
    uomm = models.ForeignKey(UOM, related_name='po_uom', on_delete=models.CASCADE, null=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='PO_ingredients', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    purchase_quantity = models.CharField(max_length=13)
    purchase_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    purchase_order = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE,null = True, blank=True )
    
    def save(self, *args, **kwargs):
        if not self.orderstatus:
            self.orderstatus = 'pending'
        
        if not self.stockreip:
            self.stockreip = generate_stockreceipt_code()
        
        super(Stock_Receipt, self).save(*args, **kwargs)

        
def generate_stockreceipt_code():
    last_stockreceipt = Stock_Receipt.objects.order_by('-id').first()
    if last_stockreceipt:
        last_stockreceipt_id = int(last_stockreceipt.stockreip.split('-')[2].strip())
        new_stockreceipt_id = last_stockreceipt_id + 1
    else:
        new_stockreceipt_id = 1
    stockreip = f"STOCKRECE-00-{str(new_stockreceipt_id).zfill(3)}"
    return stockreip


        
    
class StockRequest(models.Model):
    class TypeOfOrder(models.TextChoices):
        SALE = "Sale Order", "Sale Order"
        WORK = "Work Order", "Work Order"       
    order_type = models.CharField(max_length=12, choices=TypeOfOrder.choices, null=True)
    items = models.ManyToManyField(Item ,related_name='stock_request_items')
    item_UOM = models.ForeignKey(UOM, on_delete=models.CASCADE, related_name='item_uom_stock_request')
    consumed_quantity = models.IntegerField()
    
class StockEntry(models.Model):
    items = models.ManyToManyField(Item ,related_name='stock_entry_items')
    item_UOM = models.ForeignKey(UOM, on_delete=models.CASCADE, related_name='item_uom_stock_entry')
    quantity = models.IntegerField()
    
class BilledStock(models.Model):
    items = models.ManyToManyField(Item ,related_name='billed_stocks_items')
    item_UOM = models.ForeignKey(UOM, on_delete=models.CASCADE, related_name='item_uom_billed_stock')
    quantity = models.IntegerField()
    
class BranchTransfer(models.Model):
    from_branch = models.ForeignKey(Branch,on_delete=models.CASCADE, related_name='from_branch')
    to_branch = models.ForeignKey(Branch,on_delete=models.CASCADE, related_name='to_branch')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item',null=True)
    quantity = models.IntegerField(null=True)
    transfer_date = models.DateField(auto_now_add=True)

 
    
class BOM(models.Model):
    item = models.ForeignKey(Item, related_name='bom_item',on_delete=models.CASCADE,null=True)
    uomm = models.ForeignKey(UOM, related_name='bom_uom',on_delete=models.CASCADE,null=True)
    bom_id = models.CharField(max_length=255,unique= True)
    ingredients = models.ManyToManyField(Ingredient, related_name='bom_ingredients', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.bom_id = generate_bom_id()
        super(BOM, self).save(*args, **kwargs)
   

    
class Managepayment(models.Model):
    supplier_name = models.ForeignKey(Supplier,on_delete=models.CASCADE, related_name='suppeliername')
    
    def __str__(self):
        return self.supplier_name
    
class PaymentReports(models.Model):
    PAYMENT_MODE_CHOICES = (
        ('cash', 'Cash'),
        ('credit', 'Credit'),
        ('cheque', 'Cheque'),
        # Add other payment modes as needed
    )
    
    purchase_order = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE)
    pre_paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    paid_by = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)
    time = models.TimeField()
    stock_receipt_number = models.CharField(max_length=100)
    payment_ref_no = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    cash_voucher_no = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Payment for Purchase Order #{self.purchase_order.po_number}"
    


class Purchase_Order_Item(models.Model):
    purchase_order = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchase_quantity = models.PositiveIntegerField()
    
class Cashier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True, blank=False, unique=True, db_index=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True , related_name='namea')
    email = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    
# Create Supplier models here.
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True, blank=False, unique=True, db_index=True)
    department = models.CharField(max_length=100, null=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    id_number = models.CharField(max_length=100, null=True)
    staff_number = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return self.department
    
# Create your OrganisationalAdmin models here.
class StoreOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True, blank=False, unique=True, db_index=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    role=models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    maximum_branch = models.CharField(max_length=100)
    organisational_address = models.CharField(max_length=100)
   

    def __str__(self) -> str:
        return self.organisational_address
    
    
    # Accounting
class AssetType(models.Model):
    status = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    category = (
        ('Asset', 'Asset'),
        ('Liability', 'Liability'),
        ('Income', 'Income'),
        ('Expenses', 'Expenses'),
    )

    assert_type_ID = models.IntegerField(primary_key=True)
    short_description = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, choices=status)
    asset_category = models.CharField(max_length=100, choices=category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_description

    
class GLLine(models.Model):
    status = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    line_number = models.IntegerField(primary_key=True)
    short_description = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    update_date = models.DateField(auto_now_add=True)
    assert_type_ID = models.ForeignKey(AssetType, on_delete=models.CASCADE, null=True, blank=True)
    # master_GL_line = models.ForeignKey('accounting.GLLine', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=100, choices=status)
    current_cleared_balance = models.FloatField(default=0)
    current_uncleared_balance = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_description
    
    #Account Type
class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    abbreviation = models.CharField(max_length=10, unique=True, blank=False, null=True)
    description = models.CharField(max_length=250, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Account(models.Model):
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    gl_line_number = models.ForeignKey(GLLine, on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='gl_line_number')
    account_number = models.CharField(max_length=50, primary_key=True)
    account_description = models.CharField(max_length=100, null=True, blank=True, editable=False)
    # group_name = models.ForeignKey('Main.Group', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    opening_balance = models.FloatField(default=0)
    current_cleared_balance = models.FloatField(default=0)
    current_uncleared_balance = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_number
    
class ChargeType(models.Model):
    mode = (
        ("flat", "Flat Charge"),
        ("percentage", "Percentage"),
    )
    
    charge_type_ID = models.CharField(max_length=100, primary_key=True, null=False, blank=False)
    short_description = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)
    mode = models.CharField(max_length=100, choices=mode, default=mode[1][0])
    value = models.FloatField(default=100)
    Dr_charge_GL_category = models.CharField(max_length=100, default="NA")
    Cr_charge_GL_category = models.CharField(max_length=100, default="NA")
    create_at = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.short_description

class TransactionCode(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    short_description = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_description


class TransactionType(models.Model):
    status = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    
    mode = (
        ("percentage", "percentage"),
        ("flat", "flat"),
    )
    
    type_id = models.CharField(max_length=10, primary_key=True, default='txn-001')
    short_description = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    dr_transaction_code = models.ForeignKey(
        TransactionCode,
        on_delete=models.CASCADE,
        related_name='dr_txn_code',
        null=True,
        blank=True
    )
    dr_gl = models.ForeignKey(
        GLLine,
        on_delete=models.CASCADE,
        related_name='dr_gl',
        null=True,
        blank=True
    )
    dr_acc = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='dr_acc',
        null=True,
        blank=True
    )
    cr_transaction_code = models.ForeignKey(
        TransactionCode,
        on_delete=models.CASCADE,
        related_name='cr_txn_code',
        null=True,
        blank=True
    )
    cr_gl = models.ForeignKey(
        GLLine,
        on_delete=models.CASCADE,
        related_name='cr_gl',
        null=True,
        blank=True
    )
    cr_acc = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='cr_acc',
        null=True,
        blank=True
    )
    fee1_mode = models.CharField(max_length=10, choices=mode, default=mode[0][0])
    fee1 = models.FloatField(default=0)
    fee2_mode = models.CharField(max_length=10, choices=mode, default=mode[0][0])
    fee2 = models.FloatField(default=0)
    fee3_mode = models.CharField(max_length=10, choices=mode, default=mode[0][0])
    fee3 = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=status, default=status[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_description


    

class AccountEntry(models.Model):
    entry_ID = models.CharField(max_length=50, unique=True, blank=False, null=False)
    ENTRY_TYPE = (
        ('PL', 'PL'),
        ('AL', 'AL'),
    )
    entry_type = models.CharField(max_length=2, choices=ENTRY_TYPE, null=True, blank=True)
    transaction_ID = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True, blank=True)
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="trustee_acc_number")
    # group_name = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="trustee_belongs_group_name", null=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=10, default="KES")
    debit_credit_marker = models.CharField(max_length=100)
    exposure_date = models.DateTimeField(auto_now_add=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    posting_date = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.transaction_ID)




 










    
