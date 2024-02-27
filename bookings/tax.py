TAX_PERCENTAGE = 5
SHIPPING_CHARGES = 99
DISIGNER_CHARGES = 50

CGST_TAX = 2.5
SGST_TAX = 2.5

def calculate_taxes(amount):
    tax_charges = float(amount) * (TAX_PERCENTAGE / 100)
    return round(tax_charges, 2)

def calculate_state_and_central_tax(amount):
    tax = float(amount) * (CGST_TAX / 100)
    return  round(tax, 2)

def net_amount_without_tax(estimated_amount, shipping_charges, designer_charges):
    return round(float(estimated_amount) + float(shipping_charges) + float(designer_charges))


def calculate_net_amount(amount, tax, shipping_charges, designer_charges):
    return round((float(amount) + tax + float(shipping_charges) +  float(designer_charges)), 2)
