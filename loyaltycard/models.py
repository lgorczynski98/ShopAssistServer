from django.db import models
import os

# Create your models here.
class Loyaltycard(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    barcode_format = models.CharField(max_length=50, blank=False, null=False)
    barcode_content = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to='loyaltycards', default='loyaltycards/default.jpg')
    owner = models.ForeignKey('account.Account', related_name='loyaltycards', on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.image != self.__original_image and self.__original_image.name != 'loyaltycards/default.jpg':
            os.remove(self.__original_image.path)
            self.__original_image = self.image
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)