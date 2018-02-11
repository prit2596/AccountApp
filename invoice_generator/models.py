from django.db import models

# Create your models here.

ITEMS = (
        ('DIESEL','DIESEL'),
        ('PETROL','PETROL')
    )

class Party(models.Model):
    name = models.CharField(max_length=200,null = False, blank = False, verbose_name = 'Name')
    joining_date = models.DateField(blank = False, verbose_name = 'Joining Date')
    contact = models.BigIntegerField(blank=False,null=False, verbose_name = 'Contact')
    address = models.TextField(verbose_name = 'Address')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Party Names'

class Accounts(models.Model):
    party_id = models.ForeignKey('Party', on_delete = models.CASCADE, verbose_name = 'Party Name')
    item = models.CharField(max_length = 50, choices = ITEMS, default = 'DIESEL', verbose_name = 'Item')
    date = models.DateField(blank = False, verbose_name = 'Date')
    vehicle_no = models.CharField(max_length = 50, blank = False, verbose_name = 'Vehicle No')
    challan_no = models.IntegerField(blank = False, verbose_name = 'Challan No')
    quantity = models.DecimalField(max_digits = 10, decimal_places = 3, blank = False, verbose_name = 'Quantity')
    rate = models.DecimalField(max_digits = 5, decimal_places = 2, blank = False,  verbose_name = 'Rate')
    amount = models.DecimalField(max_digits=15, decimal_places = 2,  verbose_name = 'Amount')


    class Meta:
        verbose_name_plural = 'Accounts'

