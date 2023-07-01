# Generated by Django 4.1.4 on 2023-06-13 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_alter_product_color_alter_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
            ],
        ),
    ]