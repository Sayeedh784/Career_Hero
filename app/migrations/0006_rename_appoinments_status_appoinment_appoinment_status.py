# Generated by Django 4.0.3 on 2022-03-10 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_appoinment_req_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appoinment',
            old_name='appoinments_status',
            new_name='appoinment_status',
        ),
    ]
