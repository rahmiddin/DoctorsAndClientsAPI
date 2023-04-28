# Generated by Django 4.2 on 2023-04-28 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.PositiveIntegerField()),
                ('experience', models.PositiveIntegerField()),
                ('education', models.CharField(max_length=250)),
                ('category', models.ManyToManyField(related_name='categories', to='api.doctorcategorymodel')),
            ],
            options={
                'verbose_name': 'doctor',
                'verbose_name_plural': 'doctors',
            },
        ),
    ]
