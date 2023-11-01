# Generated by Django 4.2.4 on 2023-11-01 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0003_remove_borrow_studentid_borrow_issuerid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.CharField(max_length=10)),
                ('department', models.CharField(max_length=255)),
                ('userType', models.CharField(choices=[('Student', 'Student'), ('Facalty', 'Facalty')], default='Student', max_length=50)),
                ('userID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='faculty_id',
        ),
        migrations.RemoveField(
            model_name='students',
            name='studentID',
        ),
        migrations.RenameField(
            model_name='authors',
            old_name='firstName',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='authors',
            old_name='lastName',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='author_id',
            new_name='authorID',
        ),
        migrations.RemoveField(
            model_name='borrow',
            name='issuerID',
        ),
        migrations.RemoveField(
            model_name='borrow',
            name='issuerType',
        ),
        migrations.RemoveField(
            model_name='fines',
            name='fineID',
        ),
        migrations.RemoveField(
            model_name='fines',
            name='issueID',
        ),
        migrations.AddField(
            model_name='fines',
            name='borrowID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='library.borrow'),
        ),
        migrations.DeleteModel(
            name='BookIssues',
        ),
        migrations.DeleteModel(
            name='Faculty',
        ),
        migrations.DeleteModel(
            name='Students',
        ),
        migrations.AddField(
            model_name='borrow',
            name='userID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='library.users'),
        ),
    ]