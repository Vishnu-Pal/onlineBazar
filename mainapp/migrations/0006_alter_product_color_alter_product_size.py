# Generated by Django 4.1.4 on 2023-06-13 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_product_color_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(max_length=10),
        ),
    ]