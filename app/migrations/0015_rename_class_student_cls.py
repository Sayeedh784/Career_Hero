# Generated by Django 4.0.3 on 2022-03-16 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_rename_cls_student_class'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='Class',
            new_name='cls',
        ),
    ]