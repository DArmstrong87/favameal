# Generated by Django 3.1.3 on 2021-11-11 22:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('favamealapi', '0003_restaurant_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='favorite',
            field=models.ManyToManyField(through='favamealapi.FavoriteRestaurant', to=settings.AUTH_USER_MODEL),
        ),
    ]