from tkinter.constants import CASCADE

from django.db import models


# Create your models here.
class countrytable(models.Model):
    country=models.CharField(max_length=50, null=True)
    status=models.CharField(max_length=50, null=True)


class brandtable(models.Model):
    image=models.ImageField(null=True, upload_to="media")
    brand=models.CharField(max_length=50, null=True)
    status=models.CharField(max_length=50, null=True)

class categorytable(models.Model):
    image=models.ImageField(null=True, upload_to="media")
    category=models.CharField(max_length=50, null=True)
    status=models.CharField(max_length=50, null=True)

class productstable(models.Model):
    image=models.ImageField(null=True, upload_to="media")
    code=models.CharField(max_length=50, null=True)
    name=models.CharField(max_length=50, null=True)
    price=models.IntegerField(null=True)
    total=models.IntegerField(null=True)
    brand=models.CharField(max_length=50, null=True)
    category=models.CharField(max_length=50, null=True)
    created=models.CharField(max_length=50, null=True)
    updated=models.CharField(max_length=50, null=True)
    opening_stock=models.CharField(max_length=50, null=True)
    current_stock=models.CharField(max_length=50, null=True)
    status=models.CharField(max_length=50, null=True)


class carttable(models.Model):
    session_key=models.CharField(max_length=50, null=True)
    product=models.ForeignKey(productstable, on_delete=models.CASCADE, null=True)
    quantity=models.IntegerField(null=True)
    def totalprice(self):
        return self.quantity * self.product.total

class checkouttable(models.Model):
    session_key = models.CharField(max_length=250, null=True)
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=250, null=True)
    place = models.CharField(max_length=250, null=True)
    landmark = models.CharField(max_length=250, null=True)
    phone=models.IntegerField(null=True)
    shippingcharge = models.IntegerField(null=True)
    status = models.CharField(max_length=250, null=True)
    order_id = models.CharField(max_length=100, null=True)
    payment_method = models.CharField(max_length=100, null=True)
    total_price=models.FloatField(null=True)


class checkoutitems(models.Model):
    session_key = models.CharField(max_length=50, null=True)
    product = models.ForeignKey(productstable, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    checkout=models.ForeignKey(checkouttable,on_delete=models.CASCADE,null=True)
    def product_total(self):
        return self.quantity * self.product.total


class deliverytable(models.Model):
    name=models.CharField(max_length=250,null=True)
    mobile=models.IntegerField(null=True)
    vehicle=models.CharField(max_length=250,null=True)
    vehicle_number=models.CharField(max_length=250,null=True)


class outfordeliverytable(models.Model):
    session_key = models.CharField(max_length=250, null=True)
    delivery=models.ForeignKey(deliverytable,on_delete=models.CASCADE,null=True)
    order_id = models.CharField(max_length=100, null=True)

class contacttable(models.Model):
    name=models.CharField(max_length=250,null=True)
    email=models.CharField(max_length=250,null=True)
    subject=models.CharField(max_length=250,null=True)
    message=models.CharField(max_length=500,null=True)

