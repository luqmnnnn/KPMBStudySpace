# Generated by Django 5.0.7 on 2024-10-16 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tuition', '0005_rename_itemprice_tuitionpackage_totalprice_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tuitionpackage',
            old_name='tuitionCategory',
            new_name='itemCategory',
        ),
        migrations.RenameField(
            model_name='tuitionpackage',
            old_name='tuitionDescription',
            new_name='itemDescription',
        ),
        migrations.RenameField(
            model_name='tuitionpackage',
            old_name='tuitionID',
            new_name='itemID',
        ),
        migrations.RenameField(
            model_name='tuitionpackage',
            old_name='totalPrice',
            new_name='itemPrice',
        ),
    ]
