from django.db import models
import os

# Create your models here.
class Receipt(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    shop_name = models.CharField(max_length=100, blank=False, null=False)
    purchase_date = models.DateField()
    purchase_cost = models.FloatField()
    weeks_to_return = models.IntegerField()
    months_of_warranty = models.IntegerField()
    image = models.ImageField(upload_to='receipts', blank=False, null=False)
    thumbnail = models.ImageField(upload_to='thumbnails', default='thumbnails/default.jpg')
    owner = models.ForeignKey('account.Account', related_name='receipts', on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_thumbnail = self.thumbnail

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.thumbnail != self.__original_thumbnail and self.__original_thumbnail.name != 'thumbnails/default.jpg':
            os.remove(self.__original_thumbnail.path)
            self.__original_thumbnail = self.thumbnail
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)