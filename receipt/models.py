from django.db import models

# Create your models here.
class Receipt(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    shop_name = models.CharField(max_length=100, blank=False, null=False)
    purchase_date = models.DateField()
    purchase_cost = models.FloatField()
    return_time = models.DateField()
    warranty_time = models.DateField()
    image = models.ImageField(upload_to='receipts', blank=False, null=False)
    thumbnail = models.ImageField(upload_to='thumbnails', default='thumbnails/default.jpg')
    owner = models.ForeignKey('account.Account', related_name='receipts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title