# Generated by Django 4.2.4 on 2023-11-16 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_alter_authors_lastname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fines',
            name='datePaid',
            field=models.DateField(blank=True, null=True),
        ),
    ]
