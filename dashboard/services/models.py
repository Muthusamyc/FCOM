from django.db import models
from django.core.validators import DecimalValidator

from dashboard.master.models import User
from fcom import settings

# Create your models here.


class StichingCategory(models.Model):
    name = models.CharField(max_length=100, null=True)
    priority = models.SmallIntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class StichingService(models.Model):
    name = models.CharField(max_length=100, null=True)
    priority = models.SmallIntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class StichingFinish(models.Model):
    name = models.CharField(max_length=100, null=True)
    priority = models.SmallIntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class StichingPattern(models.Model):
    name = models.CharField(max_length=100, null=True)
    priority = models.SmallIntegerField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class StichingItem(models.Model):
    name = models.CharField(max_length=50, null=True)
    starting_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[DecimalValidator]
    )
    estimated_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[DecimalValidator]
    )
    final_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[DecimalValidator], null=True
    )
    tags = models.CharField(
        max_length=500,
        null=True,
        default="Women | Custom Stitching | Regular | Without Lining",
    )
    image = models.ImageField(
        upload_to=settings.ITEMS_IMAGE_UPLOAD_PATH, null=True)
    status = models.SmallIntegerField(default=1, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class StichingItemRelation(models.Model):
    category = models.ForeignKey(
        StichingCategory, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(
        StichingService, on_delete=models.CASCADE, null=True)
    finishing = models.ForeignKey(
        StichingFinish, on_delete=models.CASCADE, null=True)
    pattern = models.ForeignKey(
        StichingPattern, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(StichingItem, on_delete=models.CASCADE, null=True)
    sort_order = models.SmallIntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.SmallIntegerField(default=1, null=True)


class StichingTags(models.Model):
    name = models.CharField(max_length=50, null=False)
    item = models.ForeignKey(StichingItemRelation,
                             on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    priority = models.SmallIntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, null=False, unique=True
    )
    estimated_price = models.CharField(max_length=50, null=True)
    total_items = models.CharField(max_length=20, null=True)
    advance_payable = models.CharField(max_length=20, null=True)
    # 1 means cart was added, 0 cart disgarded
    status = models.SmallIntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class ItemsInCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, null=False)
    item = models.ForeignKey(
        StichingItemRelation, on_delete=models.DO_NOTHING, null=False
    )
    qty = models.SmallIntegerField(null=True)
    sub_total = models.FloatField(null=True, default=0.0)
    designer_updated_price = models.FloatField(default=0.0, null=True)
    is_cart_item_updated = models.BooleanField(null=True, default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class ServiceMode(models.Model):
    name = models.CharField(max_length=50, null=True)


class DesignerPreference(models.Model):
    name = models.CharField(max_length=50, null=True)


class EstimatedConsultationDate(models.Model):
    service_mode = models.ForeignKey(
        ServiceMode, on_delete=models.CASCADE, null=False)
    designer_preference_mode = models.ForeignKey(
        DesignerPreference, on_delete=models.CASCADE, null=False
    )
    date = models.DateField()


class Order(models.Model):

    # cart = models.ForeignKey(
    #     Cart, on_delete=models.DO_NOTHING, null=True)

    cart_id = models.IntegerField(null=True)

    generated_order_id = models.CharField(max_length=50, null=True)
    made_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

    service_type = models.ForeignKey(
        ServiceMode, on_delete=models.DO_NOTHING, null=True
    )
    booking_type = models.ForeignKey(
        DesignerPreference, on_delete=models.DO_NOTHING, null=True
    )

    designer_assigned = models.CharField(max_length=100, null=True)
    consultation_date = models.DateField(null=True)  # this also visit date
    pickup_date = models.DateField(null=True)
    inprogress_date = models.DateField(null=True)
    delivery_date = models.DateField(null=True)

    is_order_updated_by_customer = models.BooleanField(
        null=True, default=False)
    is_order_updated_by_designer = models.BooleanField(
        null=True, default=False)
    is_order_updated_by_fcom = models.BooleanField(null=True, default=False)

    # payment status flags
    is_advance_paid = models.BooleanField(null=True, default=False)
    is_estimation_paid = models.BooleanField(null=True, default=False)
    is_total_paid = models.BooleanField(null=True, default=False)

    is_updated_estimation_paid = models.BooleanField(null=True, default=False)
    is_net_amount_paid = models.BooleanField(null=True)

    is_order_approved = models.BooleanField(null=True, default=False)
    is_order_delivered = models.BooleanField(null=True, default=False)
    is_order_closed = models.BooleanField(null=True, default=False)
    is_order_cancaled = models.BooleanField(null=True, default=False)
    

    status = models.SmallIntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    invoice_date = models.DateField(null=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False)
    product_item = models.ForeignKey(
        StichingItemRelation, on_delete=models.CASCADE, null=False
    )
    qty = models.SmallIntegerField(null=True)
    sub_total = models.FloatField(null=True, default=0.0)
    designer_updated_price = models.FloatField(default=0.0, null=True)
    is_cart_item_updated = models.BooleanField(null=True, default=False)
    image = models.ImageField(
        upload_to=settings.PICKEDUP_ITEMS_IMAGE_UPLOAD_PATH, null=True)
    status = models.SmallIntegerField(null=True, default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class DesingerAssignedOrders(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True)
    designer = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    user_id = models.IntegerField(null=True)
    assinged_on = models.DateTimeField(null=True)
    status = models.SmallIntegerField(null=True)


class TransactionDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=False)
    payment_type = models.CharField(
         max_length=10, null=True)  # advance, estimated
    # payment_amount = models.CharField(max_length=50, null=True)

    estimation_paid_amount = models.FloatField(null=True, default=0.0)
    advance_paid_amount = models.FloatField(null=True, default=0.0)
    balance_amt_due = models.FloatField(null=True, default=0.0)

    # this subtotal comes from estiated price from cart
    sub_total = models.FloatField(default=0.0)
    taxable_order_amount = models.FloatField(default=0.0, null=True)
    # taxable_order_amount + tax_charges
    net_amount = models.FloatField(default=0.0)
    extra_material = models.FloatField(default=0.0)
    calcualted_tax = models.FloatField(null=True, default=0.0)
    cgst_tax_charges = models.FloatField(null=True, default=0.0)
    sgst_tax_charges = models.FloatField(null=True, default=0.0)
    igst_tax_charges = models.FloatField(null=True, default=0.0)
    shipping_charges = models.FloatField(null=True, default=0.0)
    coupon_discount = models.FloatField(null=True, default=0.0)
    designer_charges = models.FloatField(null=True, default=0.0)
    refund_amount = models.FloatField(null=True, default=0.0)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    paymtent_status = models.CharField(
        max_length=50, null=True, default="Partial Paid")
    
    


class TransactionAmount(models.Model):
    transaction = models.ForeignKey(
        TransactionDetails, on_delete=models.CASCADE, null=True
    )
    order_id = models.IntegerField(null=True)
    generated_order_id = models.CharField(max_length=50, null=True)
    payment_type = models.CharField(
        max_length=10, null=True)  # advance, estimated
    payment_amount = models.CharField(max_length=50, null=True)
    payment_gateway = models.CharField(max_length=40, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    paytm_checksum = models.CharField(max_length=500, null=True)

class PayTMTransactionDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True)
    transaction_for = models.ForeignKey(
        TransactionDetails, on_delete=models.DO_NOTHING, null=True
    )
    generated_order_id = models.CharField(max_length=50, null=True)
    payment_type = models.CharField(
        max_length=10, null=True)  # advance, estimated
    payment_amount = models.CharField(max_length=50, null=True)
    token = models.CharField(max_length=500, null=True)
    bank_name = models.CharField(max_length=500, null=True)
    bank_txn_id = models.CharField(max_length=500, null=True)
    checksum = models.CharField(max_length=500, null=True)
    currency = models.CharField(max_length=50, null=True)
    gateway_name = models.CharField(max_length=50, null=True)
    mid = models.CharField(max_length=100, null=True)
    payment_mode = models.CharField(max_length=50, null=True)
    response_code = models.CharField(max_length=50, null=True)
    response_msg = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=20, null=True)
    txn_amount = models.CharField(max_length=50, null=True)
    txn_date = models.DateTimeField(null=True)
    txn_id = models.CharField(max_length=500, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    status = models.SmallIntegerField(default=0.0, null=True)
    status_name = models.CharField(max_length=50, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(null=True)


class Area(models.Model):
    # area = models.CharField(max_length=200, null=True)
    area_name = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=50, null=True)


class PaymentMode(models.Model):
    payment_mode = models.CharField(max_length=100)
    payment_mode_description = models.CharField(max_length=2000)
    created_by = models.CharField(max_length=1)
    created_date = models.DateTimeField(null=True)
    modified_by = models.CharField(max_length=1)
    modified_date = models.DateTimeField(null=True)


class Pickup(models.Model):
    pickup_point = models.CharField(max_length=100)
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=100, null=True)


class Appointment(models.Model):
    catalogue = models.ForeignKey(
        StichingItemRelation, null=True, on_delete=models.CASCADE
    )
    area = models.ForeignKey(Area, null=True, on_delete=models.CASCADE)
    pickup = models.ForeignKey(Pickup, null=True, on_delete=models.CASCADE)


class MeasurementGroups(models.Model):
    name = models.CharField(max_length=20, null=True)
    category = models.CharField(max_length=20, null=True)


class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(OrderItems, on_delete=models.CASCADE, null=True)
    is_master = models.SmallIntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=500, null=True)
    group = models.CharField(max_length=20, null=True)


class Measurementslist(models.Model):
    measurement = models.ForeignKey(
        Measurement, on_delete=models.CASCADE, null=True)
    name = models.ForeignKey(
        MeasurementGroups, on_delete=models.CASCADE, null=True)
    size = models.CharField(max_length=10, null=True)
    unit = models.CharField(max_length=10, default="in")


class CustomerReview(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=True)
    designer = models.SmallIntegerField(null=True)
    customer_services = models.SmallIntegerField(null=True)
    delivery_services = models.SmallIntegerField(null=True)
    review = models.CharField(max_length=500, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
