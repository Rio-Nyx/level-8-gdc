# Generated by Django 4.0.1 on 2022-03-01 07:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_report_last_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='new_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')], default='PENDING', max_length=100),
        ),
        migrations.AlterField(
            model_name='history',
            name='old_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')], default='PENDING', max_length=100),
        ),
        migrations.AlterField(
            model_name='report',
            name='send_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
