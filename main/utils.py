import random, string
from django.utils.crypto import get_random_string
from main.models import *

last_three_digits_company = 0
last_three_digits_branch = 0
last_three_digits_itemgroup = 0
last_three_digits_itemcategory = 0
last_three_digits_itemcode = 0
last_three_digits_bom = 0
last_three_digits_rec = 0

# def generate_stockreceiopt_code():
#     global last_three_digits_stockreceiopt
#     last_three_digits_stockreceiopt += 1
#     stockreip = 'STOCKRECE-00- ' + str(last_three_digits_stockreceiopt).zfill(3)
#     print(stockreip)
#     return stockreip


def generate_company_code():
    global last_three_digits_company
    last_three_digits_company += 1
    company_code = "COMPN-00- " + str(last_three_digits_company).zfill(3)
    return company_code


def generate_Branch_code():
    from main.models import Branch

    global last_three_digits_branch
    last_three_digits_branch += 1
    branch_code = "BRANCH-00-" + str(last_three_digits_branch).zfill(3)

    # Check if the generated code already exists
    while Branch.objects.filter(branch_code=branch_code).exists():
        last_three_digits_branch += 1
        branch_code = "BRANCH-00-" + str(last_three_digits_branch).zfill(3)

    return branch_code


def generate_itemgroup_code():
    global last_three_digits_itemgroup
    last_three_digits_itemgroup += 1
    group_code = "IteGRO-00- " + str(last_three_digits_itemgroup).zfill(3)
    return group_code


# def generate_itemcategory():
#     category_code = 'ITCAT-00- ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
#     return category_code


def generate_itemcategory(pre_id):
    last_three_digits_itemcategory = int(pre_id)
    last_three_digits_itemcategory += 1
    category_code = "ITCATE-00-" + str(last_three_digits_itemcategory).zfill(3)
    return category_code


# def generate_itemcode():
#     global last_three_digits_itemcode
#     last_three_digits_itemcode += 1
#     category_code = 'ITCODE-00-' + str(last_three_digits_itemcode).zfill(3)
#     return category_code


# def generate_itemcode():
#     item_code = 'IteCODE-00- ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
#     return item_code


def generate_po_number():
    global last_three_digits_ponumber
    last_three_digits_ponumber += 1
    po_number = "PO-NUM-00-" + str(last_three_digits_ponumber).zfill(3)
    return po_number


def generate_bom_id():
    global last_three_digits_bom
    last_three_digits_bom += 1
    bom_id = "PO-NUM-00-" + str(last_three_digits_bom).zfill(3)
    return bom_id


# def generate_bom_id():
#     bom_id = 'BOMID-00- ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
#     return bom_id
# def generate_account_number():

#     account_number = int(get_random_string(length=8, allowed_chars='1234567890'))
#     account_number = 'ACC' + '-' + str(account_number)
#     check_acc = Account.objects.filter(account_number__iexact=account_number).exists()
#     if check_acc:
#         generate_account_number(acc_pre)
#     return account_number

# def generate_receipt_number():


#     # Generate a UUID (Universally Unique Identifier)
#     unique_id = uuid.uuid4().hex
#     # Combine the prefix "REC-" with the UUID to create the receipt number
#     receipt_number = f"REC-{unique_id}"
#     return receipt_number
def generate_receipt_number():
    global last_three_digits_rec
    last_three_digits_rec += 1
    receipt_number = "REC-00-" + str(last_three_digits_rec).zfill(3)
    return receipt_number
