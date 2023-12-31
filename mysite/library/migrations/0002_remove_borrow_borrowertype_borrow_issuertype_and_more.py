# Generated by Django 4.2.4 on 2023-11-01 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrow',
            name='BorrowerType',
        ),
        migrations.AddField(
            model_name='borrow',
            name='issuerType',
            field=models.CharField(choices=[('Student', 'Student'), ('Facalty', 'Facalty')], default='Available', max_length=50),
        ),
        migrations.AlterField(
            model_name='bookissues',
            name='issuerType',
            field=models.CharField(choices=[('Student', 'Student'), ('Facalty', 'Facalty')], default='Available', max_length=50),
        ),
        migrations.AlterField(
            model_name='books',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Checked Out', 'Checked Out'), ('Reserved', 'Reserved')], max_length=50),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Checked Out', 'Checked Out'), ('Reserved', 'Reserved')], max_length=50),
        ),
    ]
