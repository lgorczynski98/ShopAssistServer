# Generated by Django 2.1.15 on 2020-08-05 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('shop_name', models.CharField(max_length=100)),
                ('purchase_date', models.DateField()),
                ('purchase_cost', models.FloatField()),
                ('weeks_to_return', models.IntegerField()),
                ('months_of_warranty', models.IntegerField()),
                ('image', models.ImageField(upload_to='receipts')),
                ('thumbnail', models.ImageField(default='thumbnails/default.jpg', upload_to='thumbnails')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
