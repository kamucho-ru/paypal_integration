# Generated by Django 2.2.1 on 2020-09-29 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20200929_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('U', 'Urgent'), ('HP', 'High (pending)'), ('UP', 'Urgent (pending)')], default='L', max_length=20),
        ),
    ]
