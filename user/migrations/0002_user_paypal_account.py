# Generated by Django 2.2.1 on 2020-10-04 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='paypal_account',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]