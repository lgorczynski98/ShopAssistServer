from django.db import models

# Create your models here.
class Loyaltycard(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    barcode_format = models.CharField(max_length=50, blank=False, null=False)
    barcode_content = models.CharField(max_length=100, blank=False, null=False)
    image_url = models.URLField(blank=False, null=False)
    owner = models.ForeignKey('account.Account', related_name='loyaltycards', on_delete=models.CASCADE)

    def __str__(self):
        return self.title