# Generated by Django 4.2 on 2023-04-28 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_doctorcategorymodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='category',
            field=models.ManyToManyField(related_name='categorys', to='api.doctorcategorymodel'),
        ),
    ]