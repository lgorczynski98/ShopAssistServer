# Generated by Django 3.0.6 on 2020-06-05 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyaltycard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loyaltycard',
            name='image_url',
        ),
        migrations.AddField(
            model_name='loyaltycard',
            name='image',
            field=models.ImageField(default='loyaltycards/default.jpg', upload_to='loyaltycards'),
        ),
    ]