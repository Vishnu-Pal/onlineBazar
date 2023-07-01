# Generated by Django 4.1.4 on 2023-06-19 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_alter_product_color_alter_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.IntegerField()),
                ('shipping', models.IntegerField()),
                ('final', models.IntegerField()),
                ('mode', models.CharField(max_length=20)),
                ('orderstatus', models.IntegerField(choices=[(0, 'Cancle'), (1, 'Not Packed'), (2, 'Packed'), (3, 'Out For Delivery'), (4, 'Delevered')], default=1)),
                ('paymentstatus', models.IntegerField(choices=[(1, 'Pending'), (2, 'Done')], default=1)),
                ('rppid', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('rpoid', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('rpsid', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('size', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('qyt', models.IntegerField()),
                ('total', models.IntegerField()),
                ('pic', models.ImageField(upload_to='')),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.checkout')),
            ],
        ),
    ]