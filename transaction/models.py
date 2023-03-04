from django.db import models

# Create your models here.
class Transaction(models.Model):
    TYPE_TRANSACTION_CHOICES = [
        ('sell', 'sell'),
        ('buy', 'buy'),
    ]
    symbol = models.CharField(max_length=255, db_index=True)
    order_id = models.CharField(max_length=255, db_index=True)
    price = models.FloatField()
    amount = models.FloatField(null=False)
    time_stamp = models.IntegerField()
    type = models.CharField(max_length=4, choices=TYPE_TRANSACTION_CHOICES, default='sell')
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.order_id)

