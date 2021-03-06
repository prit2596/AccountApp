# Generated by Django 2.0.1 on 2018-02-03 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(choices=[('DIESEL', 'DIESEL'), ('PETROL', 'PETROL')], default='DIESEL', max_length=50, verbose_name='Item')),
                ('date', models.DateField(verbose_name='Date')),
                ('vehicle_no', models.CharField(max_length=50, verbose_name='Vehicle No')),
                ('challan_no', models.IntegerField(verbose_name='Challan No')),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Quantity')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Rate')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Amount')),
            ],
            options={
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('joining_date', models.DateField(verbose_name='Joining Date')),
                ('contact', models.BigIntegerField(verbose_name='Contact')),
                ('address', models.TextField(verbose_name='Address')),
            ],
            options={
                'verbose_name_plural': 'Party Names',
            },
        ),
        migrations.AddField(
            model_name='accounts',
            name='party_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice_generator.Party', verbose_name='Party Name'),
        ),
    ]
