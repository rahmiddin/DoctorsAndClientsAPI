# Generated by Django 4.2 on 2023-04-28 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_doctor_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='category',
            field=models.ManyToManyField(related_name='categories', to='api.doctorcategorymodel'),
        ),
    ]
